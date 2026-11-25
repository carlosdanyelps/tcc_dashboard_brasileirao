import { Routes, Route} from "react-router-dom";
import Home from "./pages/Home/index";
import Graphics from "./pages/Graphics/index";
import Classification from "./pages/Classification/index";
import PlayersCoaches from "./pages/PlayersCoaches/index";
import HeadToHead from "./pages/HeadToHead/index";
import CurrentSeason from "./pages/CurrentSeason/index";

function MainRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/graphics" element={<Graphics />} />
            <Route path="/classification" element={<Classification />} />
            <Route path="/players-coaches" element={<PlayersCoaches />} />
            <Route path="/head-to-head" element={<HeadToHead />} />
            <Route path="/current-season" element={<CurrentSeason />} />
        </Routes>
    );
}

export default MainRoutes;