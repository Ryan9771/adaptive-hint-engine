import { useRef, useState } from "react";
import { Editor, OnMount } from "@monaco-editor/react";
import style from "../../util/Styles";
import { RunBtn, ResetBtn } from "../Buttons";

function CodeBox() {
  const MIN_HEIGHT = 150;
  const MAX_HEIGHT = 400;
  const LINE_HEIGHT = 20;

  const editorRef = useRef<any>(null);
  const [editorHeight, setEditorHeight] = useState(MIN_HEIGHT);

  // Define a custom theme
  const defineCustomTheme = (monaco: any) => {
    monaco.editor.defineTheme("customTheme", {
      base: "vs-dark", // Use the dark base theme
      inherit: true, // Inherit default vs-dark settings
      rules: [], // Define any syntax-specific styling here
      colors: {
        "editor.background": "#212936", // Set custom background color
      },
    });
  };

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;

    // Dynamically Adjusts height based on content
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
    const defaultCode =
      "# Write your code here\nage = \nname = \nis_student = ";
    if (editorRef.current) {
      editorRef.current.setValue(defaultCode);
      setEditorHeight(MIN_HEIGHT);
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
          language="kotlin"
          theme="vs-dark"
          value={"# Write your code here\nage = \nname = \nis_student = "}
          onMount={handleEditorDidMount}
          options={{
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
        {/* <button
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        onClick={resetCode}
      ></button> */}
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
