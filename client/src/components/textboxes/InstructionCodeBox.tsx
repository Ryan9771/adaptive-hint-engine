import style from "../../util/Styles";
import CodeBox from "./CodeBox";
import { useState } from "react";
import Markdown from "react-markdown";
import { TestResult } from "../../util/Types";

interface Props {
  title: string;
  text: string;
  skelCode: string;
  previousCode: string;
  studentCode: string;
  language: string;
  setStudentCode: (code: string) => void;
  setHintTitle: (title: string) => void;
  output: string;
  setOutput: (output: string) => void;
  error: string;
  setError: (error: string) => void;
  testResults: TestResult[];
  setTestResults: (results: TestResult[]) => void;
}
function InstructionCodeBox({
  title,
  text,
  skelCode,
  studentCode,
  previousCode,
  language,
  setStudentCode,
  setHintTitle,
  output,
  setOutput,
  error,
  setError,
  testResults,
  setTestResults,
}: Props) {
  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "title")}>{title}</div>
      <div className={style(styles, "txt")}>
        <Markdown>{text}</Markdown>
      </div>
      <div className={style(styles, "txt")}>
        <Markdown>
          Click the `Run` button to run your code or the `Test` button to test
          your code with our test cases!
        </Markdown>
      </div>
      <CodeBox
        previousCode={previousCode}
        skelCode={skelCode}
        studentCode={studentCode}
        language={language}
        setStudentCode={setStudentCode}
        setOutput={setOutput}
        setError={setError}
        setTestResults={setTestResults}
        setHintTitle={setHintTitle}
      />

      {output && (
        <div className={style(styles, "outputBox")}>
          <div className={style(styles, "outputErrorTitles")}>Output:</div>
          <pre>{output}</pre>
        </div>
      )}

      {error && (
        <div className={style(styles, "errorBox")}>
          <div className={style(styles, "outputErrorTitles")}>Error:</div>
          <pre>{error}</pre>
        </div>
      )}

      {testResults.length > 0 && (
        <div className={style(styles, "testResultWrapper")}>
          {testResults.map((t, idx) => (
            <div
              key={idx}
              className={`${style(styles, "testResultBox")} ${
                t.passed
                  ? style(styles, "testResultPassed")
                  : style(styles, "testResultFailed")
              }`}
            >
              <div className={style(styles, "testResultText")}>
                <div>
                  <b>Input:</b> {JSON.stringify(t.input)}
                </div>
                <div>
                  <b>Expected:</b> {JSON.stringify(t.expected)}
                </div>
                <div>
                  <b>Actual:</b> {JSON.stringify(t.actual)}
                </div>
                {!t.passed && <div className="font-bold">❌ Test Failed</div>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  ctn: [
    "flex",
    "flex-col",
    "w-full",
    "p-4",
    "bg-white",
    "shadow-sm",
    "gap-4",
    "rounded-md",
  ],
  outputBox: [
    "mt-4",
    "p-4",
    "bg-gray-800",
    "text-white",
    "font-mono",
    "text-sm",
    "rounded-md",
    "overflow-x-auto",
  ],
  errorBox: [
    "mt-4",
    "p-4",
    "bg-red-100",
    "text-red-800",
    "font-mono",
    "text-sm",
    "rounded-md",
    "overflow-x-auto",
  ],
  outputErrorTitles: ["font-bold", "mb-2"],
  txt: ["text-text-default", "leading-5", "md:leading-6"],
  title: ["font-semibold", "lg:text-lg"],
  testResultWrapper: ["mt-4", "space-y-3"],
  testResultBox: ["p-4", "rounded-md", "border"],
  testResultText: ["text-sm", "font-mono", "mt-1"],
  testResultPassed: ["bg-green-100", "border-green-400", "text-green-800"],
  testResultFailed: ["bg-red-100", "border-red-400", "text-red-800"],
};

export default InstructionCodeBox;
