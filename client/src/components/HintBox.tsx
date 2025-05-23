import style from "../util/Styles";
import { FaRegLightbulb, FaSpinner } from "react-icons/fa";
import { getHint } from "../util/util";
import Markdown from "react-markdown";
import { useState } from "react";
import { TestResult } from "../util/types";

interface Props {
  hintTitle: string;
  studentName: string;
  exerciseId: string;
  studentCode: string;
  error: string;
  setError: (error: string) => void;
  setOutput: (output: string) => void;
  testResults: TestResult[];
  setTestResults: (results: TestResult[]) => void;
}

function HintBox({
  studentName,
  hintTitle,
  exerciseId,
  studentCode,
  error,
  testResults,
  setError,
  setOutput,
  setTestResults,
}: Props) {
  const [hintText, setHintText] = useState(
    "Click here to reveal a helpful hint for solving this exercise"
  );

  const [isLoading, setIsLoading] = useState(false);
  const [showRating, setShowRating] = useState(false);
  const [selectedRating, setSelectedRating] = useState<number | null>(null);

  const generateHint = async () => {
    setIsLoading(true);

    try {
      setTestResults([]);
      setError("");
      setOutput("");
      const hint = await getHint(
        studentName,
        exerciseId,
        studentCode,
        error,
        testResults
      );
      setHintText(hint);
      setShowRating(true);
    } catch (e) {
      setHintText("I wasn't able to generate a hint. Please try again!");
      setShowRating(false);
    }
    setIsLoading(false);
  };

  const handleRatingClick = (rating: number) => {
    setSelectedRating(rating);
    setShowRating(false);
    // TODO: Send to backend
    console.log(selectedRating);
  };

  return (
    <div className={style(styles, "ctn")} onClick={generateHint}>
      <div className={style(styles, "titleDiv")}>
        {isLoading ? (
          <FaSpinner className={style(styles, "spinner")} />
        ) : (
          <FaRegLightbulb className={style(styles, "icon")} />
        )}
        <div className={style(styles, "title")}>{hintTitle}.</div>
      </div>
      <div className={style(styles, "txt")}>
        <Markdown>{isLoading ? "Generating a hint..." : hintText}</Markdown>
      </div>
      {showRating && (
        <div className={style(styles, "ratingCtn")}>
          <p className={style(styles, "txt")}>
            How helpful was this hint based on your progress so far?
          </p>
          {[1, 2, 3, 4, 5].map((num) => (
            <button
              key={num}
              onClick={(e) => {
                e.stopPropagation();
                handleRatingClick(num);
              }}
              className={style(styles, "rating")}
            >
              {num}
            </button>
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
  rating: [
    "w-6",
    "h-6",
    "rounded-full",
    "border",
    "border-hint-title",
    "text-hint-title",
    "hover:bg-hint-title",
    "hover:text-white",
    "transition-all",
    "duration-150",
    "text-sm",
  ],
  ratingCtn: ["flex", "gap-2", "pt-2", "items-center"],
};

export default HintBox;
