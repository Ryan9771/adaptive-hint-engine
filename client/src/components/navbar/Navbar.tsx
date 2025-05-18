import style from "../../util/Styles";
import ProfileCtn from "./ProfileCtn";

function Navbar() {
  return (
    <div className={style(styles, "ctn")}>
      <ProfileCtn />
    </div>
  );
}

const styles = {
  ctn: [
    "w-full",
    "flex",
    "items-center",
    "p-4",
    "border",
    "border-border",
    "lg:hidden",
  ],
  icon: ["w-6", "h-6", "fill-icon-fill", "cursor-pointer"],
};

export default Navbar;
