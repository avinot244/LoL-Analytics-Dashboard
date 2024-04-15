import '../styles/App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Home from "./Home"
import ChampionOverview from "./ChampionOverview"
import PlayerOverview from "./PlayerOverview"
import GameOverview from './GameOverview';
import Monitoring from './Monitoring';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
	{
		path:'/',
		element: <Home />
	},
	{
		path:'/ChampionOverview/Scrims',
		element: <ChampionOverview />
	},
	{
		path:'/ChampionOverview/Esports',
		element: <ChampionOverview />
	},
	{
		path:'/PlayerOverview/Scrims',
		element: <PlayerOverview/>
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
		path:'/Monitoring',
		element: <Monitoring/>
	}
])

function App() {
	return <RouterProvider router={router}/>
}

export default App;
