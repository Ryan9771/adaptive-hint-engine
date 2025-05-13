import style from "../util/Styles";
import Navbar from "../components/navbar/Navbar";
import ExercisePath from "../components/ExercisePath";
import BasicTextBox from "../components/textboxes/BasicTextBox";
import InstructionCodeBox from "../components/textboxes/InstructionCodeBox";
import HintBox from "../components/HintBox";
import Sidebar from "../components/sidebar/Sidebar";

/* Would eventually need to pass in exercise data */
function ExercisePython2() {
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
    "Think of a list like a guestbook at a busy event—sometimes, people sign in more than once by mistake. As the host, you want a clean record showing who actually attended, without counting anyone twice. Before we tackle the code to remove duplicates from a list, picture yourself flipping through those entries, keeping only the first signature from each guest and crossing out the rest. The goal? A list that's accurate, neat, and clutter-free."

const instructionCodeBoxText = `
Return a list of numbers without any duplicates. Eg:

remove_duplicates([1, 1, 1, 2, 2, 2]) should equal [1, 2]`

const skelCode = `
def remove_duplicates(numbers: list[int]) -> list[int]:
    list_without_duplicates = []

    return list_without_duplicates`

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

export default ExercisePython2;
