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
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import SignInSide from './Home/Login';

const router = createBrowserRouter([
	{
		path:'/',
		element: <SignInSide />
	},
	{
		path:'/Home',
		element: <Home />
	},
	{
		path:'/ChampionOverview/Scrims',
		element: <ChampionOverviewScrim />
	},
	{
		path:'/ChampionOverview/Esports',
		element: <ChampionOverview />
	},
	{
		path:'/PlayerOverview/Scrims',
		element: <PlayerOverviewScrim/>
	},
	{
		path:'/PlayerOverview/Esports',
		element: <PlayerOverview/>
	},
	{
		path:'/GameOverview/Scrims',
		element: <GameOverview/>
	},
	{
		path:'/GameOverview/Esports',
		element: <GameOverview/>
	},
	{
		path:'/Monitoring/Download',
		element: <Downloader/>
	},
	{
		path:'/Monitoring/PCAMaker',
		element: <PCAModelMaker/>
	},
	{
		path:'/Monitoring/PCAOverview',
		element: <PCAModelOverview/>
	}
])

function App() {
	return <RouterProvider router={router}/>
}

export default App;
