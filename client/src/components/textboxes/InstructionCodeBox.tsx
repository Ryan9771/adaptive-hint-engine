import style from "../../util/Styles";
import CodeBox from "./CodeBox";

interface Props {
  title: string;
  text: string;
  skelCode: string;
  previousCode: string;
  language: string;
  setStudentCode: (code: string) => void;
}
function InstructionCodeBox({
  title,
  text,
  skelCode,
  previousCode,
  language,
  setStudentCode,
}: Props) {
  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "title")}>{title}</div>
      <div className={style(styles, "txt")}>{text}</div>
      <CodeBox
        previousCode={previousCode}
        skelCode={skelCode}
        language={language}
        setStudentCode={setStudentCode}
      />
    </div>
  );
}

const styles = {
  ctn: [
    "flex",
    "flex-col",
    "w-full",
    "p-4",
    "bg-white",
    "shadow-sm",
    "gap-4",
    "rounded-md",
  ],
  txt: ["text-text-default", "leading-5", "md:leading-6"],
  title: ["font-semibold", "lg:text-lg"],
};

export default InstructionCodeBox;
