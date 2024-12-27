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
  ctn: ["flex", "w-full", "p-4", "bg-white", "shadow-sm", "rounded-md"],
  txt: ["text-text-default", "leading-5"],
};

export default BasicTextBox;
