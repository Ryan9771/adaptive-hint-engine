import { HashRouter, Routes, Route } from "react-router-dom";
import Exercise from "./pages/Exercise";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Exercise />} />
      </Routes>
    </HashRouter>
  );
}

export default App;
