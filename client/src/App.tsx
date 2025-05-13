import { HashRouter, Routes, Route } from "react-router-dom";
import Exercise from "./pages/ExerciseInitial";
import ExercisePython1 from "./pages/ExercisePython1";
import ExercisePython2 from "./pages/ExercisePython2";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Exercise />} />
        <Route path="/exercise/python/exercise1" element={<ExercisePython1 />} />
        <Route path="/exercise/python/exercise2" element={<ExercisePython2 />} />
        {/* <Route path="/exercise/:language/:exercise" element={<Exercise />} /> */}
        <Route path="*" element={<p>404</p>} />
      </Routes>
    </HashRouter>
  );
}

export default App;
