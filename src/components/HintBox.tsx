import style from "../util/Styles";
import { FaRegLightbulb } from "react-icons/fa";

function HintBox() {
  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "titleDiv")}>
        <FaRegLightbulb className={style(styles, "icon")} />
        <div className={style(styles, "title")}>Need a hint?</div>
      </div>
      <p className={style(styles, "txt")}>
        Click here to reveal a helpful hint for solving this exercise.
      </p>
    </div>
  );
}

const styles = {
  ctn: [
    "flex",
    "flex-col",
    "w-full",
    "p-4",
    "border",
    "border-hint-border",
    "bg-hint",
    "gap-3",
  ],
  titleDiv: ["flex", "gap-3", "items-center"],
  title: ["text-hint-title", "font-medium"],
  icon: ["h-4", "fill-hint-title"],
  txt: ["text-hint-text", "text-sm"],
};

export default HintBox;
