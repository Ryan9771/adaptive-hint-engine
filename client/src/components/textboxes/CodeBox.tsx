import { useRef, useState } from "react";
import { Editor, OnMount } from "@monaco-editor/react";
import style from "../../util/Styles";
import { RunBtn, ResetBtn } from "../Buttons";
import { resetPreviousCode } from "../../util/util";
import { useParams } from "react-router-dom";

interface Props {
  skelCode: string;
  previousCode: string;
  language: string;
  setStudentCode: (code: string) => void;
}
function CodeBox({ skelCode, previousCode, language, setStudentCode }: Props) {
  const MIN_HEIGHT = 150;
  const MAX_HEIGHT = 400;
  const LINE_HEIGHT = 20;

  const editorRef = useRef<any>(null);
  const [editorHeight, setEditorHeight] = useState(MIN_HEIGHT);

  const { lang, exercise } = useParams();
  const exerciseId = `${lang}_${exercise}`;

  // Define a custom theme
  const defineCustomTheme = (monaco: any) => {
    monaco.editor.defineTheme("customTheme", {
      base: "vs-dark",
      inherit: true,
      rules: [],
      colors: {
        "editor.background": "#212936",
      },
    });
  };

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;

    // Adjust height of the codebox based on code length
    const updateHeight = () => {
      const lineCount = editor.getModel()?.getLineCount() || 1;
      const newHeight = Math.min(
        Math.max(lineCount * LINE_HEIGHT, MIN_HEIGHT),
        MAX_HEIGHT
      );

      setEditorHeight(newHeight);
    };

    editor.onDidContentSizeChange(updateHeight);

    // Adjust height on mount
    updateHeight();

    defineCustomTheme(monaco);
    monaco.editor.setTheme("customTheme");
  };

  const resetCode = () => {
    const defaultCode = skelCode;
    if (editorRef.current) {
      editorRef.current.setValue(defaultCode);
      setEditorHeight(MIN_HEIGHT);
      resetPreviousCode(exerciseId, defaultCode);
    }
  };

  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "btnCtn")}>
        <RunBtn handleBtn={resetCode} />
        <ResetBtn handleBtn={resetCode} />
      </div>
      <div
        className={style(styles, "editorCtn")}
        style={{
          height: `${editorHeight}px`,
        }}
      >
        <Editor
          height="100%"
          language={language}
          theme="vs-dark"
          value={previousCode}
          onMount={handleEditorDidMount}
          onChange={(value) => setStudentCode(value || "")}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            lineNumbers: "on",
            scrollBeyondLastLine: false,
            wordWrap: "on",
            scrollbar: {
              vertical: editorHeight === MAX_HEIGHT ? "auto" : "hidden",
            },
            padding: { top: 20 },
          }}
        />
      </div>
    </div>
  );
}

const styles = {
  ctn: ["flex", "flex-col", "bg-editor-blue", "p-4", "gap-4", "rounded-lg"],
  btnCtn: ["flex", "items-center", "justify-end", "gap-5"],
  editorCtn: ["flex", "flex-col", "w-full", "rounded-md", "overflow-hidden"],
};

export default CodeBox;
