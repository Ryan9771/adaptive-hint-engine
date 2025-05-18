import style from "../util/Styles";
import { FaRegLightbulb, FaSpinner } from "react-icons/fa";
import { getHint } from "../util/util";
import Markdown from "react-markdown";
import { useState } from "react";

interface Props {
  exerciseId: string;
  studentCode: string;
}

function HintBox({ exerciseId, studentCode }: Props) {
  const [hintText, setHintText] = useState(
    "Click here to reveal a helpful hint for solving this exercise"
  );

  const [isLoading, setIsLoading] = useState(false);

  const generateHint = async () => {
    setIsLoading(true);

    try {
      const hint = await getHint(exerciseId, studentCode);
      setHintText(hint);
    } catch (e) {
      setHintText("I wasn't able to generate a hint. Please try again!");
    }
    setIsLoading(false);
  };

  return (
    <div className={style(styles, "ctn")} onClick={generateHint}>
      <div className={style(styles, "titleDiv")}>
        {isLoading ? (
          <FaSpinner className="animate-spin h-4 w-4 text-hint-title" />
        ) : (
          <FaRegLightbulb className={style(styles, "icon")} />
        )}
        <div className={style(styles, "title")}>Need a hint? Click here</div>
      </div>
      <div className={style(styles, "txt")}>
        <Markdown>{isLoading ? "Generating a hint..." : hintText}</Markdown>
      </div>
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
    "rounded-md",
    "cursor-pointer",
  ],
  titleDiv: ["flex", "gap-3", "items-center"],
  title: ["text-hint-title", "font-medium"],
  icon: ["h-4", "fill-hint-title"],
  spinner: ["animate-spin", "h-4", "w-4", "text-hint-title"],
  txt: ["text-hint-text", "text-sm"],
};

export default HintBox;
