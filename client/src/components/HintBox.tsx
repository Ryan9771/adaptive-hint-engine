import style from "../util/Styles";
import { FaRegLightbulb, FaSpinner } from "react-icons/fa";
import { getHint } from "../util/util";
import Markdown from "react-markdown";
import { useState } from "react";
import { TestResult } from "../util/types";
import { logEvaluation } from "../util/util";

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

  const [simpleHintText, setSimpleHintText] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [showRating, setShowRating] = useState(false);

  const [hintRating, setHintRating] = useState<number | null>(null);
  const [simpleHintRating, setSimpleHintRating] = useState<number | null>(null);

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
      setHintText(hint.hint);
      setSimpleHintText(hint.simpleHint);

      setShowRating(true);
    } catch (e) {
      setHintText("I wasn't able to generate a hint. Please try again!");
      setShowRating(false);
    }
    setIsLoading(false);
  };

  const sendRatings = () => {
    logEvaluation(
      studentName,
      exerciseId,
      hintRating || 0,
      simpleHintRating || 0,
      hintText,
      simpleHintText
    );
    setHintRating(null);
    setSimpleHintRating(null);
  };

  const handleHintRating = (rating: number) => {
    setHintRating(rating);

    if (rating && simpleHintRating) {
      setShowRating(false);
      sendRatings();
    }
  };

  const handleSimpleHintRating = (rating: number) => {
    setSimpleHintRating(rating);
    if (rating && hintRating) {
      setShowRating(false);
      sendRatings();
    }
  };

  const getRatingClass = (active: boolean) =>
    `${style(styles, "rating")} ${
      active
        ? "bg-hint-title text-white"
        : "text-hint-title hover:bg-hint-title hover:text-white"
    }`;

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
                handleHintRating(num);
              }}
              className={getRatingClass(hintRating === num)}
            >
              {num}
            </button>
          ))}
        </div>
      )}

      <div className={style(styles, "txt")}>{isLoading ? "" : "--------"}</div>

      {simpleHintText && (
        <>
          <div className={style(styles, "txt")}>
            <Markdown>{isLoading ? "" : simpleHintText}</Markdown>
          </div>

          {showRating && (
            <div className={style(styles, "ratingCtn")}>
              <p className={style(styles, "txt")}>How helpful was this hint?</p>
              {[1, 2, 3, 4, 5].map((num) => (
                <div
                  key={num}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSimpleHintRating(num);
                  }}
                  className={getRatingClass(simpleHintRating === num)}
                >
                  {num}
                </div>
              ))}
            </div>
          )}
        </>
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
    "transition-all",
    "duration-150",
    "text-sm",
    "flex",
    "items-center",
    "justify-center",
    "cursor-pointer",
    "text-hint-title",
  ],
  ratingCtn: ["flex", "gap-2", "pt-2", "items-center"],
};

export default HintBox;
