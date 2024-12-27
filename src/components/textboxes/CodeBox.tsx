import { useRef, useState } from "react";
import { Editor, OnMount } from "@monaco-editor/react";

function CodeBox() {
  const MIN_HEIGHT = 150;
  const MAX_HEIGHT = 400;
  const LINE_HEIGHT = 20;

  const editorRef = useRef<any>(null);
  const [editorHeight, setEditorHeight] = useState(MIN_HEIGHT);

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
    <div
      className={"flex flex-col w-full rounded-md overflow-hidden"}
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
          scrollbar: { vertical: "hidden", horizontal: "hidden" },
        }}
      />
      {/* <button
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        onClick={resetCode}
      ></button> */}
    </div>
  );
}

export default CodeBox;
