import { HashRouter, Routes, Route } from "react-router-dom";
import Exercise from "./pages/Exercise";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<p>Home page</p>} />
        <Route
          path="/exercise/:studentName/:lang/:exercise"
          element={<Exercise />}
        />
        <Route path="*" element={<p>404</p>} />
      </Routes>
    </HashRouter>
  );
}

export default App;
