import { Routes, Route} from "react-router-dom";
import Home from "./pages/Home/index";
import Graphics from "./pages/Graphics/index";
import Classification from "./pages/Classification/index";

function MainRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/graphics" element={<Graphics />} />
            <Route path="/classification" element={<Classification />} />
        </Routes>
    );
}

export default MainRoutes;