import style from "../../util/Styles";
import profileImg from "/src/assets/images/profile.png";

function ProfileCtn() {
  return (
    <div className={style(styles, "ctn")}>
      <img
        className={style(styles, "img")}
        src={profileImg}
        alt="profile pic"
      />
      <p className={style(styles, "txt")}>rkp21</p>
    </div>
  );
}

const styles = {
  ctn: ["flex", "items-center", "gap-3", "cursor-pointer"],
  img: ["w-10", "rounded-full"],
  txt: ["font-semibold"],
};

export default ProfileCtn;
