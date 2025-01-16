import '../styles/App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Home from "./Home/Home"
import ChampionOverview from "./ChampionOverview/ChampionOverview"
import ChampionOverviewScrim from './ChampionOverview/ChampionOverviewScrim';
import PlayerOverview from "./PlayerOverview/PlayerOverview"
import PlayerOverviewScrim from "./PlayerOverview/PlayerOverviewScrim"
import GameOverview from './GameOverview/GameOverview';
import Downloader from './Monitoring/Downloader';
import PCAModelMaker from './Monitoring/PCAModelMaker';
import PCAModelOverview from './Monitoring/PCAModelOverview';
import PCADocumentation from './PlayerOverview/Documentation'
import RefreshDBComp from './Monitoring/RefreshDBComp';
import ScoutingPlayer from './PlayerOverview/Scouting'
import TeamAnalysisOverall from './TeamAnalysis/TeamAnalysisOverall';
import TeamAnalysisDetails from './TeamAnalysis/TeamAnalysisDetails';
import TestComp from './TestComp';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SignInSide from './Home/Login';
import PrivateRoute from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import GetTokenComp from './GetToken/GetTokenComp';



function App() {
	return (
		<BrowserRouter>
			<AuthProvider>
				<Routes>
					<Route Component={SignInSide} path='/' exact/>
					<Route element={<PrivateRoute />}>
						<Route element={<Home />} path='/Home' exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<ChampionOverviewScrim />} path="/ChampionOverview/Scrims" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<ChampionOverview />} path="/ChampionOverview/Esports" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<PlayerOverviewScrim />} path="/PlayerOverview/Scrims" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<PlayerOverview />} path="/PlayerOverview/Esports" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<ScoutingPlayer />} path="/PlayerOverview/Scouting" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<GameOverview />} path="/GameOverview/Scrims" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<GameOverview />} path="/GameOverview/Esports" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<Downloader />} path="/Monitoring/Download" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<PCAModelMaker />} path="/Monitoring/PCAMaker" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<PCAModelOverview />} path="/Monitoring/PCAOverview" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<GetTokenComp />} path="/GetToken" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<PCADocumentation />} path="/PlayerOverview/Docs" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<RefreshDBComp />} path="/Monitoring/RefreshDB" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<TestComp/>} path="/Monitoring/TestComp" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<TeamAnalysisOverall/>} path="/teamAnalysisOverall" exact/>
					</Route>
					<Route element={<PrivateRoute />}>
						<Route element={<TeamAnalysisDetails/>} path="/teamAnalysisDetails" exact/>
					</Route>
					
				</Routes>
			</AuthProvider>
		</BrowserRouter>
		
	)
}

export default App;
