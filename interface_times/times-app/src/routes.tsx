import { Routes, Route} from "react-router-dom";
import Home from "./pages/Home/index";
import Graphics from "./pages/Graphics/index";
import Classification from "./pages/Classification/index";
<<<<<<< HEAD
=======
import PlayersCoaches from "./pages/PlayersCoaches/index";
import HeadToHead from "./pages/HeadToHead/index";
<<<<<<< HEAD
>>>>>>> parent of 87020e5 (sla)
=======
>>>>>>> parent of 87020e5 (sla)

function MainRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/graphics" element={<Graphics />} />
            <Route path="/classification" element={<Classification />} />
<<<<<<< HEAD
=======
            <Route path="/players-coaches" element={<PlayersCoaches />} />
            <Route path="/head-to-head" element={<HeadToHead />} />
<<<<<<< HEAD
>>>>>>> parent of 87020e5 (sla)
=======
>>>>>>> parent of 87020e5 (sla)
        </Routes>
    );
}

export default MainRoutes;