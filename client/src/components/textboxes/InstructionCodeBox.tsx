import style from "../../util/Styles";
import CodeBox from "./CodeBox";
import { useState } from "react";

export interface TestResult {
  name: string;
  input: any;
  expected: any;
  actual: any;
  passed: boolean;
}

interface Props {
  title: string;
  text: string;
  skelCode: string;
  previousCode: string;
  studentCode: string;
  language: string;
  setStudentCode: (code: string) => void;
}
function InstructionCodeBox({
  title,
  text,
  skelCode,
  studentCode,
  previousCode,
  language,
  setStudentCode,
}: Props) {
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [testResults, setTestResults] = useState<TestResult[]>([]);

  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "title")}>{title}</div>
      <div className={style(styles, "txt")}>{text}</div>
      <CodeBox
        previousCode={previousCode}
        skelCode={skelCode}
        studentCode={studentCode}
        language={language}
        setStudentCode={setStudentCode}
        setOutput={setOutput}
        setError={setError}
        setTestResults={setTestResults}
      />

      {testResults.length > 0 && (
        <div className="mt-4 space-y-3">
          {testResults.map((t, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-md border ${
                t.passed
                  ? "bg-green-100 border-green-400 text-green-800"
                  : "bg-red-100 border-red-400 text-red-800"
              }`}
            >
              <div className="font-semibold">{t.name}</div>
              <div className="text-sm font-mono mt-1">
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
};

export default InstructionCodeBox;
