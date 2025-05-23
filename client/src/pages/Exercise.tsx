import style from "../util/Styles";
import Navbar from "../components/navbar/Navbar";
import ExercisePath from "../components/ExercisePath";
import BasicTextBox from "../components/textboxes/BasicTextBox";
import InstructionCodeBox from "../components/textboxes/InstructionCodeBox";
import HintBox from "../components/HintBox";
import Sidebar from "../components/sidebar/Sidebar";
import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getExerciseDetails } from "../util/util";
import { TestResult } from "../util/types";

function Exercise() {
  const { studentName, lang, exercise } = useParams();
  const [exerciseTitle, setExerciseTitle] = useState("");
  const [exerciseDescription, setExerciseDescription] = useState("");
  const [exerciseText, setExerciseText] = useState("");
  const [skelCode, setSkelCode] = useState("");
  const [previousCode, setPreviousCode] = useState("");
  const [studentCode, setStudentCode] = useState(previousCode);
  const [hintTitle, setHintTitle] = useState(defaultHintTitle);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [testResults, setTestResults] = useState<TestResult[]>([]);

  const exerciseId = `${lang}_${exercise}`;

  const navigate = useNavigate();

  useEffect(() => {
    if (!studentName || !lang || !exercise) {
      console.error("Missing required parameters");
      navigate("/404");
      return;
    }

    const fetchExerciseDetails = async () => {
      const exerciseDetails = await getExerciseDetails(studentName, exerciseId);
      if (exerciseDetails.exerciseExists) {
        setExerciseTitle(exerciseDetails.exerciseTitle);
        setExerciseDescription(exerciseDetails.exerciseDescription);
        setExerciseText(exerciseDetails.exerciseText);
        setSkelCode(exerciseDetails.skelCode);
        setPreviousCode(exerciseDetails.previousCode);
      } else {
        console.log("Exercise does not exist");
        navigate("/404");
      }
    };

    fetchExerciseDetails();

    console.log(studentCode);
  }, [lang, exercise]);

  return (
    <div className={style(styles, "ctn")}>
      <Navbar />
      <Sidebar />
      <div className={style(styles, "bodyCtn")}>
        <div className={style(styles, "exerciseBody")}>
          <ExercisePath
            exerciseTitle={exerciseTitle.toLowerCase().replace(/ /g, "_")}
          />
          <p className={style(styles, "title")}>{exerciseTitle}</p>

          <BasicTextBox text={exerciseDescription} />

          <InstructionCodeBox
            title="Instructions"
            text={exerciseText}
            skelCode={skelCode}
            studentCode={studentCode}
            previousCode={previousCode}
            language={language}
            setStudentCode={setStudentCode}
            setHintTitle={setHintTitle}
            output={output}
            setOutput={setOutput}
            error={error}
            setError={setError}
            testResults={testResults}
            setTestResults={setTestResults}
          />

          <HintBox
            hintTitle={hintTitle}
            studentName={studentName!}
            exerciseId={exerciseId}
            studentCode={studentCode}
            error={error}
            setError={setError}
            setOutput={setOutput}
            testResults={testResults}
            setTestResults={setTestResults}
          />
        </div>
      </div>
    </div>
  );
}

export const defaultHintTitle =
  "This hint adapts — click anytime to get help based on what you've done so far.";

const language = "python";

const styles = {
  ctn: ["flex", "w-full", "flex-col", "h-full", "items-center", "lg:flex-row"],
  bodyCtn: [
    "w-full",
    "h-full",
    "flex",
    "flex-col",
    "items-center",
    "p-4",
    "border",
    "border-border",
    "gap-5",
    "overflow-y-scroll",
  ],
  exerciseBody: [
    "w-full",
    "flex",
    "flex-col",
    "gap-6",
    "max-w-screen-lg",
    "pb-12",
    "lg:gap-8",
  ],
  title: ["text-2xl", "font-bold", "leading-7"],
};

export default Exercise;
