import style from "../../util/Styles";
import ProfileCtn from "./ProfileCtn";
import { CgProfile } from "react-icons/cg";

function Navbar() {
  return (
    <div className={style(styles, "ctn")}>
      <ProfileCtn />
      <CgProfile className="w-16 h-16" />
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
    "lg:hidden",
  ],
  icon: ["w-6", "h-6", "fill-icon-fill", "cursor-pointer"],
};

export default Navbar;
