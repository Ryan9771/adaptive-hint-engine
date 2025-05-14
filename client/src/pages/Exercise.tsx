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
          <p className={style(styles, "title")}>
            Higher Order Functions in Kotlin
          </p>

          <BasicTextBox text={basicTextBoxText} />

          <InstructionCodeBox
            title="Instructions"
            text={instructionCodeBoxText}
            code={skelCode}
            language={language}
          />

          <HintBox />
        </div>
      </div>
    </div>
  );
}

const basicTextBoxText =
  "Kotlin includes a lot of powerful features from functional languages like Haskell. One of the main features that we think of being characteristic of a functional language is the ability to use higher-order functions. Try this out in the exercises below. ";

const instructionCodeBoxText =
  "Add a method 'includes' to class Circle to determine whether a certain point is inside or outside the circle.";

const skelCode = "def fizzbuzz(n: int):\n\tpass";

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
    // "lg:items-start",
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
