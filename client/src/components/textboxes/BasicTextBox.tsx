import style from "../../util/Styles";

interface Props {
  text: string;
}
function BasicTextBox({ text }: Props) {
  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "txt")}>{text}</div>
    </div>
  );
}

const styles = {
  ctn: [
    "flex",
    "w-full",
    "p-4",
    "bg-white",
    "shadow-sm",
    "rounded-md",
    "lg:bg-transparent",
    "lg:p-0",
    "lg:shadow-none",
  ],
  txt: ["text-text-default", "leading-5", "md:leading-6"],
};

export default BasicTextBox;
