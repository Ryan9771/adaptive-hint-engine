import style from "../../util/Styles";
import ProfileCtn from "./ProfileCtn";
import { IoMdExit } from "react-icons/io";

function Navbar() {
  return (
    <div className={style(styles, "ctn")}>
      <ProfileCtn />
      <IoMdExit className={style(styles, "icon")} />
    </div>
  );
}

const styles = {
  ctn: [
    "w-full",
    "flex",
    "justify-between",
    "items-center",
    "p-4",
    "border",
    "border-border",
  ],
  icon: ["w-6", "h-6", "fill-icon-fill", "cursor-pointer"],
};

export default Navbar;
