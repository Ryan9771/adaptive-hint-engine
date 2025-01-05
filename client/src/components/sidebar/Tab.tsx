import style from "../../util/Styles";
import { FaCode } from "react-icons/fa";
import { IoMdExit } from "react-icons/io";

interface Props {
  active: boolean;
  text: string;
}

function Tab({ active, text }: Props) {
  function icon(isActive: boolean, text: string) {
    let classes = style(styles, "icon");

    if (isActive) {
      classes = classes + "fill-active-blue";
    } else {
      classes = classes + "fill-icon-fill";
    }

    if (text === "Exercises") {
      return <FaCode className={classes} />;
    } else {
      return <IoMdExit className={classes} />;
    }
  }

  let ctnClass = style(styles, "ctn");
  let txtClass = style(styles, "txt");

  if (active) {
    ctnClass = ctnClass + "bg-active-tab";
    txtClass = txtClass + "text-active-blue";
  } else {
    txtClass = txtClass + "text-icon-fill";
  }

  return (
    <div className={ctnClass}>
      {icon(active, text)}
      <p className={txtClass}>{text}</p>
    </div>
  );
}

const styles = {
  ctn: [
    "flex",
    "p-2.5",
    "gap-2.5",
    "items-center",
    "rounded-md",
    "cursor-pointer",
    "xl:w-full",
  ],
  icon: ["w-10"],
  txt: ["text-sm", "font-medium", "hidden", "xl:block"],
};

export default Tab;
