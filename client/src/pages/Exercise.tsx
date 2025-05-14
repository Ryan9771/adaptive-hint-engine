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

/* Would eventually need to pass in exercise data */
function Exercise() {
  const { lang, exercise } = useParams();
  const [exerciseTitle, setExerciseTitle] = useState(exercise);
  const [exerciseDescription, setExerciseDescription] = useState("");
  const [exerciseText, setExerciseText] = useState("");
  const [skelCode, setSkelCode] = useState("");

  console.log(`Exercise Id: ${lang}_${exercise}`);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchExerciseDetails = async () => {
      const exerciseDetails = await getExerciseDetails(`${lang}_${exercise}`);
      if (exerciseDetails.exerciseExists) {
        setExerciseTitle(exerciseDetails.exerciseTitle);
        setExerciseDescription(exerciseDetails.exerciseDescription);
        setExerciseText(exerciseDetails.exerciseText);
        setSkelCode(exerciseDetails.skelCode);
        console.log(exerciseDetails);
      } else {
        console.log("Exercise does not exist");
        navigate("/404");
      }
    };

    fetchExerciseDetails();
  }, [lang, exercise]);

  return (
    <div className={style(styles, "ctn")}>
      <Navbar />
      <Sidebar />
      <div className={style(styles, "bodyCtn")}>
        <div className={style(styles, "exerciseBody")}>
          <ExercisePath />
          <p className={style(styles, "title")}>{exerciseTitle}</p>

          <BasicTextBox text={exerciseDescription} />

          <InstructionCodeBox
            title="Instructions"
            text={exerciseText}
            code={skelCode}
            language={language}
          />

          <HintBox />
        </div>
      </div>
    </div>
  );
}

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
  ],
  exerciseBody: [
    "w-full",
    "flex",
    "flex-col",
    "gap-6",
    "max-w-screen-lg",
    "lg:gap-8",
  ],
  title: ["text-2xl", "font-bold", "leading-7"],
};

export default Exercise;
