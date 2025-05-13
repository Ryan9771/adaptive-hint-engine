import style from "../util/Styles";
import Navbar from "../components/navbar/Navbar";
import ExercisePath from "../components/ExercisePath";
import BasicTextBox from "../components/textboxes/BasicTextBox";
import InstructionCodeBox from "../components/textboxes/InstructionCodeBox";
import HintBox from "../components/HintBox";
import Sidebar from "../components/sidebar/Sidebar";

/* Would eventually need to pass in exercise data */
function ExercisePython1() {
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
    `Imagine you're counting out loud with friends, but to make it fun, you add a twist: every time you hit a number divisible by 3, you say “Fizz” instead, and for 5, it's “Buzz.” For numbers divisible by both, it's “FizzBuzz!” It's a simple game that tests attention and logic—just like how a small change in rules can make basic counting a bit more interesting. Lets bring that logic into code.`

const instructionCodeBoxText = "Description: Print numbers from 1 to n. For multiples of 3, print \"Fizz\", for multiples of 5, print \"Buzz\", and for multiples of both, print \"FizzBuz\"."

const skelCode = "def fizzbuzz(n: int):\n\tpass"

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

export default ExercisePython1;
