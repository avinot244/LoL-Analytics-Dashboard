import '../styles/App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Home from "./Home"
import ChampionOverview from "./ChampionOverview"
import PlayerOverview from "./PlayerOverview"
import GameOverview from './GameOverview';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
	{
		path:'/',
		element: <Home />
	},
	{
		path:'/ChampionOverview',
		element: <ChampionOverview />
	},
	{
		path:'/PlayerOverview',
		element: <PlayerOverview/>
	},
	{
		path:'/GameOverview',
		element: <GameOverview/>
	}
])

function App() {
	return <RouterProvider router={router}/>
}

export default App;
