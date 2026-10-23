import { EditorState, EditorSelection, Compartment, Prec } from '@codemirror/state';
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, drawSelection } from '@codemirror/view';
import { defaultKeymap, history, historyKeymap, indentMore, indentLess } from '@codemirror/commands';
import { isolateHistory, undo, redo, cursorCharLeft, cursorCharRight, cursorLineUp, cursorLineDown, cursorLineStart, cursorLineEnd, selectCharLeft, selectCharRight, selectLineUp, selectLineDown, selectLineStart, selectLineEnd, insertNewlineAndIndent, deleteCharBackward } from '@codemirror/commands';
import { indentOnInput, bracketMatching, defaultHighlightStyle, syntaxHighlighting, indentUnit } from '@codemirror/language';
import { python } from '@codemirror/lang-python';
import { cpp } from '@codemirror/lang-cpp';
import { autocompletion, closeBrackets, closeBracketsKeymap, completionStatus, acceptCompletion, startCompletion, closeCompletion, moveCompletionSelection, snippet, hasNextSnippetField, nextSnippetField, hasPrevSnippetField, prevSnippetField } from '@codemirror/autocomplete';

const words = {
  python: ['False','None','True','and','as','assert','async','await','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield','print','input','range','len','int','str','float','list','dict','set','tuple','enumerate','zip','sum','min','max','sorted'],
  c: ['auto','break','case','char','const','continue','default','do','double','else','enum','extern','float','for','if','int','long','register','return','short','signed','sizeof','static','struct','switch','typedef','union','unsigned','void','volatile','while','printf','scanf','malloc','free','puts','strlen'],
  cpp: ['auto','bool','break','case','char','class','const','continue','default','do','double','else','enum','false','float','for','if','int','long','namespace','new','nullptr','private','protected','public','return','short','signed','sizeof','static','struct','switch','template','this','true','typedef','typename','unsigned','using','vector','string','sort','cin','cout','endl','while']
};
const snippets = {
  python: [
    ['for', 'for ${item} in ${iterable}:\n    ${pass}'],
    ['if', 'if ${condition}:\n    ${pass}'],
    ['def', 'def ${name}(${args}):\n    ${pass}'],
    ['while', 'while ${condition}:\n    ${pass}']
  ],
  c: [
    ['for', 'for (int ${i} = 0; ${i} < ${n}; ${i}++) {\n    ${}\n}'],
    ['if', 'if (${condition}) {\n    ${}\n}'],
    ['main', 'int main(void) {\n    ${}\n    return 0;\n}']
  ],
  cpp: [
    ['for', 'for (int ${i} = 0; ${i} < ${n}; ${i}++) {\n    ${}\n}'],
    ['if', 'if (${condition}) {\n    ${}\n}'],
    ['main', 'int main() {\n    ${}\n    return 0;\n}']
  ]
};

function options(lang) {
  const plain = (words[lang] || []).map(label => ({ label, type: /^(print|input|range|len|int|str|float|list|dict|set|tuple|enumerate|zip|sum|min|max|sorted|printf|scanf|malloc|free|puts|strlen|sort)$/.test(label) ? 'function' : 'keyword' }));
  const blocks = (snippets[lang] || []).map(([label, template]) => ({ label, type: 'snippet', detail: '代码片段', apply: snippet(template) }));
  return [...blocks, ...plain];
}

export function mountEditor({ parent, doc, lang, onChange }) {
  let currentLang = lang;
  /* 「Esc 后按 Tab 离开编辑器」的开关。
     CodeMirror 把 Tab 吃掉了（用来接受补全 / 缩进），于是键盘用户会被关在编辑器里。
     约定：按一下 Esc 先把这道门打开，紧接着按 Tab 就交给浏览器去移动焦点；
     一旦又敲了字（文档变了）就自动收回这个开关，免得隔了一会儿 Tab 变成意外跳走。 */
  let escapeArmed = false;
  const language = new Compartment();
  const completionSource = context => {
    const word = context.matchBefore(/[A-Za-z_][A-Za-z_0-9]*/);
    if (!word || (word.from === word.to && !context.explicit)) return null;
    return { from: word.from, options: options(currentLang), validFor: /^[A-Za-z_][A-Za-z_0-9]*$/ };
  };
  const completionKeys = Prec.highest(keymap.of([
    { key: 'Tab', run: view => {
        if (escapeArmed) { escapeArmed = false; return false; }   /* 放行 → 浏览器默认行为（移出焦点） */
        return completionStatus(view.state) === 'active' && acceptCompletion(view)
            || hasNextSnippetField(view.state) && nextSnippetField(view)
            || indentMore(view); } },
    { key: 'Shift-Tab', run: view => hasPrevSnippetField(view.state) ? prevSnippetField(view) : indentLess(view) },
    { key: 'Ctrl-Space', run: startCompletion },
    { key: 'ArrowDown', run: view => completionStatus(view.state) === 'active' && moveCompletionSelection(true)(view) },
    { key: 'ArrowUp', run: view => completionStatus(view.state) === 'active' && moveCompletionSelection(false)(view) },
    { key: 'Escape', run: view => {
        const open = completionStatus(view.state) === 'active';
        if (open) closeCompletion(view);
        escapeArmed = true;      /* 有补全时＝关掉提示；没有时＝单纯解锁，两种都武装 */
        return open; } }         /* 无补全时返回 false，让 Esc 继续冒泡 */
  ]));
  const view = new EditorView({
    state: EditorState.create({
      doc,
      extensions: [
        lineNumbers(), highlightActiveLineGutter(), highlightActiveLine(), drawSelection(),
        history(), indentOnInput(), bracketMatching(), closeBrackets(),
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
        language.of(lang === 'python' ? python() : cpp()),
        indentUnit.of('    '), EditorState.tabSize.of(4),
        autocompletion({ override: [completionSource], activateOnTyping: true, defaultKeymap: false }),
        completionKeys,
        keymap.of([...closeBracketsKeymap, ...historyKeymap, ...defaultKeymap]),
        EditorView.updateListener.of(update => {
          if (update.docChanged) { escapeArmed = false; onChange(update.state.doc.toString()); }
        })
      ]
    }),
    parent
  });
  return {
    getValue: () => view.state.doc.toString(),
    mobileEdit(action, value, selecting = false) {
      if (!['undo','redo'].includes(action)) view.dispatch({annotations:isolateHistory.of('full')});
      const moves = selecting
        ? {left:selectCharLeft,right:selectCharRight,up:selectLineUp,down:selectLineDown,home:selectLineStart,end:selectLineEnd}
        : {left:cursorCharLeft,right:cursorCharRight,up:cursorLineUp,down:cursorLineDown,home:cursorLineStart,end:cursorLineEnd};
      const command = moves[action] || {indent:indentMore,outdent:indentLess,undo,redo,newline:insertNewlineAndIndent,backspace:deleteCharBackward}[action];
      if (command) command(view);
      else if (action === 'insert') {
        const pairs = {'(' : ')', '[' : ']', '{' : '}', '"' : '"', "'" : "'"};
        const close = pairs[value];
        view.dispatch({ ...view.state.changeByRange(range => {
          const selected = view.state.sliceDoc(range.from, range.to);
          const insert = value + (close ? selected + close : '');
          return {changes:{from:range.from,to:range.to,insert}, range:close
            ? EditorSelection.range(range.from + value.length, range.from + value.length + selected.length)
            : EditorSelection.cursor(range.from + insert.length)};
        }), userEvent:'input.mobile', scrollIntoView:true });
      }
      view.focus();
    },
    setLanguage(next) {
      if (next === currentLang) return;
      currentLang = next;
      view.dispatch({ effects: language.reconfigure(next === 'python' ? python() : cpp()) });
    },
    destroy: () => view.destroy(),
    view
  };
}
