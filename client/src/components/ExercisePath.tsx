import style from "../util/Styles";
import { IoMdHome } from "react-icons/io";

/* Will take in the exercise path from higher level component */
function ExercisePath() {
  return (
    <div className={style(styles, "ctn")}>
      <IoMdHome className={style(styles, "icon")} />
      <p className={style(styles, "txt")}>/</p>
      <p className={style(styles, "txt") + "cursor-pointer"}>
        Higher Order Functions
      </p>
    </div>
  );
}

const styles = {
  ctn: ["flex", "items-center", "py-2.5", "gap-2.5", "w-full"],
  icon: ["w-4", "fill-icon-fill", "cursor-pointer"],
  txt: ["fill-text-default", "text-sm"],
};

export default ExercisePath;
