import style from "../../util/Styles";
import pfp from "/src/assets/images/profile.png";
import Tab from "./Tab";

function Sidebar() {
  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "profileCtn")}>
        <img className={style(styles, "pfp")} src={pfp} alt="pfp" />
        <div className={style(styles, "pfpTextCtn")}>
          <p className={style(styles, "pfpText")}>Ryan Patel</p>
          <p className={style(styles, "pfpShortCode")}>rkp21</p>
        </div>
        <div className={style(styles, "tabCtn")}>
          <Tab active={true} text="Exercises" />
          <Tab active={false} text="Logout" />
        </div>
      </div>
    </div>
  );
}

const styles = {
  ctn: [
    "lg:w-24",
    "xl:w-60",
    "h-full",
    "bg-white",
    "flex-col",
    "items-center",
    "px-2.5",
    "py-8",
    "border",
    "border-border",
    "gap-2.5",
    "flex-shrink-0",
    "hidden",
    "lg:block",
  ],
  profileCtn: ["flex", "flex-col", "items-center", "w-full", "gap-5"],
  pfp: ["w-14", "xl:w-24"],
  pfpTextCtn: ["w-full", "flex", "flex-col", "items-center", "gap-1"],
  pfpText: ["text-sm", "font-medium", "text-black", "hidden", "xl:block"],
  pfpShortCode: ["text-xs", "font-medium", "text-text-default"],
  tabCtn: ["py-5", "gap-5", "w-full", "flex", "flex-col", "items-center"],
};

export default Sidebar;
