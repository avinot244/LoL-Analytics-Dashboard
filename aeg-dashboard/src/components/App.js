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
import { BrowserRouter, createBrowserRouter, Routes, Route } from 'react-router-dom';
import SignInSide from './Home/Login';
import { Fragment, useState } from 'react';
import NavBarComp from './NavbarComp';
import PrivateRoute from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';



function App() {
	const [loggedIn, setLoggedIn] = useState(false)


	const router = createBrowserRouter([
		{
			path:'/',
			element: <SignInSide loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
		},
		{
			path:'/Home',
			element: (
				<PrivateRoute><Home loggedIn={loggedIn} setLoggedIn={setLoggedIn}/></PrivateRoute>
			)
		},
		{
			path:'/ChampionOverview/Scrims',
			element: <PrivateRoute><ChampionOverviewScrim loggedIn={loggedIn} setLoggedIn={setLoggedIn}/></PrivateRoute>
		},
		{
			path:'/ChampionOverview/Esports',
			element: <ChampionOverview loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/PlayerOverview/Scrims',
			element: <PlayerOverviewScrim loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/PlayerOverview/Esports',
			element: <PlayerOverview loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/GameOverview/Scrims',
			element: <GameOverview loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/GameOverview/Esports',
			element: <GameOverview loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/Monitoring/Download',
			element: <Downloader loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/Monitoring/PCAMaker',
			element: <PCAModelMaker loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		},
		{
			path:'/Monitoring/PCAOverview',
			element: <PCAModelOverview loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>//
		}
	])
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
				</Routes>
			</AuthProvider>
		</BrowserRouter>
		
	)
}

export default App;
