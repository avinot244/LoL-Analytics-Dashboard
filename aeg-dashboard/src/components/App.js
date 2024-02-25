import '../styles/App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import BasicExample from "./NavbarComp";
import Home from "./Home"
import LinkPage from "./LinkPage"
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
	{
		path:'/',
		element: <Home />
	},
	{
		path:'/link',
		element : <LinkPage />
	}
])

function App() {
	return <RouterProvider router={router}/>
}

export default App;
