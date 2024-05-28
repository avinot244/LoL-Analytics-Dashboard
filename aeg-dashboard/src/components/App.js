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
import { useState, useEffect } from 'react';



function App() {
	const [loggedIn, setLoggedIn] = useState(false)


	const router = createBrowserRouter([
		{
			path:'/',
			element: <SignInSide loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
		},
		{
			path:'/Home',
			element: <Home loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/ChampionOverview/Scrims',
			element: <ChampionOverviewScrim loggedIn={loggedIn}/>//
		},
		{
			path:'/ChampionOverview/Esports',
			element: <ChampionOverview loggedIn={loggedIn}/>//
		},
		{
			path:'/PlayerOverview/Scrims',
			element: <PlayerOverviewScrim loggedIn={loggedIn}/>//
		},
		{
			path:'/PlayerOverview/Esports',
			element: <PlayerOverview loggedIn={loggedIn}/>//
		},
		{
			path:'/GameOverview/Scrims',
			element: <GameOverview loggedIn={loggedIn}/>//
		},
		{
			path:'/GameOverview/Esports',
			element: <GameOverview loggedIn={loggedIn}/>//
		},
		{
			path:'/Monitoring/Download',
			element: <Downloader loggedIn={loggedIn}/>//
		},
		{
			path:'/Monitoring/PCAMaker',
			element: <PCAModelMaker loggedIn={loggedIn}/>//
		},
		{
			path:'/Monitoring/PCAOverview',
			element: <PCAModelOverview loggedIn={loggedIn}/>//
		}
	])
	return <RouterProvider router={router}/>
}

export default App;
