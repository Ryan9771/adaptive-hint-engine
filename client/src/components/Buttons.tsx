import style from "../util/Styles";
import { FaPlay } from "react-icons/fa";
import { RiResetLeftFill } from "react-icons/ri";

interface Props {
  handleBtn: () => void;
}

export function RunBtn({ handleBtn }: Props) {
  return (
    <div className={style(styles, "runBtnCtn")} onClick={() => handleBtn()}>
      <FaPlay className="h-3.5 fill-white" />
      <p className="text-sm text-white">Run</p>
    </div>
  );
}

export function ResetBtn({ handleBtn }: Props) {
  return (
    <div className={style(styles, "resetBtnCtn")} onClick={() => handleBtn()}>
      <RiResetLeftFill className="h-3.5 fill-reset-gray" />
      <p className="text-sm text-reset-gray">Reset</p>
    </div>
  );
}

const styles = {
  runBtnCtn: [
    "flex",
    "items-center",
    "px-2",
    "py-1",
    "bg-run-blue",
    "justify-center",
    "gap-2",
    "rounded-md",
    "cursor-pointer",
  ],
  resetBtnCtn: [
    "flex",
    "items-center",
    "px-2",
    "py-1",
    "justify-center",
    "gap-2",
    "cursor-pointer",
  ],
};
