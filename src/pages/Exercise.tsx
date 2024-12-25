import style from "../util/Styles";
import Navbar from "../components/navbar/Navbar";

/* Would eventually need to pass in exercise data */
function Exercise() {
  return (
    <div className={style(styles, "ctn")}>
      <Navbar />
    </div>
  );
}

const styles = {
  ctn: ["flex", "w-full", "flex-col", "h-full", "items-center"],
};

export default Exercise;
