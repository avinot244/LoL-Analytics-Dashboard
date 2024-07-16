import "../../styles/PCADocumentation.css"
import NavBarComp from "../utils/NavbarComp"
import top_challenger from "../../assets/top_challenger.png"
import jungle_challenger from "../../assets/jungle_challenger.png"
import mid_challenger from "../../assets/middle_challenger.png"
import bot_challenger from "../../assets/bot_challenger.png"
import support_challenger from "../../assets/support_challenger.png"

import { Typography, Stack, Card, CardMedia, CardContent, Avatar, Box, Button } from "@mui/material"
import Divider from "@mui/material/Divider";
import InfoIcon from '@mui/icons-material/Info';

function PCADocumentation({loggedIn, setLoggedIn}) {
    return (
        <div className="wrapper-PCAdocumentation">
            <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10}}>
                Player Analysis Documentation
            </Typography>
            
            <Typography id="PCADocumentation-top-title" variant="h3" component="h1" align="left" sx={{ml:5, mt: 10}}>
                Top lane
            </Typography>
            <Typography id="PCADocumentation-top" variant="p" component="div" align="left" sx={{ml:10, mr: 10, mb: 10, fontSize: 25}}>
                <ul className="PCADocumentation-top">
                    <li className="PCADocumentation-top-content">
                        <span className="factor-name">Aggressive:</span> Tendency of the given player to perform kills, assists and hence having a good kill participation percentage. It is also computed with considering the damage per minute the player is doing.
                    </li>
                    <li>
                        <span className="factor-name">Farming Safely:</span> Ability of the given player to gather resources, whether it is with his CS per minutes or having an experience/gold advantage while mitigating his amount of deaths.
                    </li>
                    <li>
                        <span className="factor-name">Playing w/ jungle:</span> Tendency of the given player to let go his lane and roam in his topside jungle or river while being somewhat close to his jungler.
                    </li>
                    <li>
                        <span className="factor-name">Objective/Towers:</span> Tendency of the player to inflict damage on towers and/or objectives?
                    </li>
                    <li>
                        <span className="factor-name">Playing Alone:</span> Factor that measures how much the player is not the closest to his jungler while farming and placing vision.
                    </li>
                    <li>
                        <span className="factor-name">Invader:</span> Tendency of the given player to invade the enemy jungle.
                    </li>
                </ul>
            </Typography>

            <Divider
                style={{ background: 'white', borderWidth: 1}}
                variant="middle"
            />

            <Typography id="PCADocumentation-jungle-title" variant="h3" component="h1" align="left" sx={{ml:5, mt: 10}}>
                Jungle
            </Typography>
            <Typography id="PCADocumentation-jungle" variant="p" component="div" align="left" sx={{ml:10, mr: 10, mb: 10, fontSize: 25}}>
                <ul className="PCADocumentation-jungle">
                    <li className="PCADocumentation-jungle-content">
                        <span className="factor-name">Invader:</span> Tendency of the given player to leave his jungle and play inside the enemy jungle
                    </li>
                    <li className="PCADocumentation-jungle-content">
                        <span className="factor-name">Aggressive:</span> Ability of the player to perform kills/assists and having a significant damage per minute to generate a gold lead
                    </li>
                    <li className="PCADocumentation-jungle-content">
                        <span className="factor-name">Skirmish:</span> Ability of the player to have a high assist rate as well as kill participation and damage per minute. Which clearly tells if he is involved in skirmishes.
                    </li>
                    <li className="PCADocumentation-jungle-content">
                        <span className="factor-name">Farming Safely:</span> Tendency of the player to gather resources and generate a gold/experience lead while mitigating his amount of deaths.
                    </li>
                    <li className="PCADocumentation-jungle-content">
                        <span className="factor-name">Playing Botside:</span> Ability of the player to play inside the enemy botside jungle and botside river. 
                    </li>
                    <li className="PCADocumentation-jungle-content">
                        <span className="factor-name">Playing Topside:</span> Ability of the player to play around the top lane.
                    </li>
                </ul>

            </Typography>

            <Divider
                style={{ background: 'white', borderWidth: 1}}
                variant="middle"
            />

            <Typography id="PCADocumentation-midlane-title" variant="h3" component="h1" align="left" sx={{ml:5, mt: 10}}>
                Mid lane
            </Typography>
            <Typography id="PCADocumentation-midlane" variant="p" component="div" align="left" sx={{ml:10, mr: 10, mb: 10, fontSize: 25}}>
                <ul className="PCADocumentation-midlane">
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Farming Safely:</span> Ability of the given player to gather resources, whether it is with his CS per minutes or having an experience/gold advantage while mitigating his amount of deaths.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Aggressive:</span> Tendency of the given player to perform kills, assists and hence having a good kill participation percentage. It is also computed with considering the damage per minute the player is doing.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Roaming bot:</span> Tendency of the given player to leave his lane and wandering around bot lane.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Objective/Towers:</span> Tendency of the player to inflict damage on towers and/or objectives.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Skirmish</span> Tendency of the player to have a high amount of assists as well as kill participation and damage per minute. Which clearly indicates that he is involved in skirmishes a lot.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Invader:</span> Tendency of the given player to invade the enemy jungle.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Vision River:</span> Ability of the player to place or kill wards while being in the river.
                    </li>
                    <li className="PCADocumentation-midlane-content">
                        <span className="factor-name">Roaming Top:</span> Tendency of the given player to leave his lane and wandering around the top river/lane.
                    </li>
                </ul>
            </Typography>

            <Divider
                style={{ background: 'white', borderWidth: 1}}
                variant="middle"
            />

            <Typography id="PCADocumentation-ADC-title" variant="h3" component="h1" align="left" sx={{ml:5, mt: 10}}>
                ADC
            </Typography>
            <Typography id="PCADocumentation-ADC" variant="p" component="div" align="left" sx={{ml:10, mr: 10, mb: 10, fontSize: 25}}>
                <ul className="PCADocumentation-ADC">
                    <li className="PCADocumentation-ADC-content">
                        <span className="factor-name">Aggressive:</span> Tendency of the given player to perform kills, assists and hence having a good kill participation percentage. It is also computed with considering the damage per minute the player is doing.
                    </li>
                    <li className="PCADocumentation-ADC-content">
                        <span className="factor-name">Lane Player:</span> Tendency of having a good cs per minute and generating an experience lead while staying in his lane.
                    </li>
                    <li className="PCADocumentation-ADC-content">
                        <span className="factor-name">Farming Safely:</span> Ability of the given player to gather resources, whether it is with his CS per minutes or having an experience/gold advantage while mitigating his amount of deaths.
                    </li>
                    <li className="PCADocumentation-ADC-content">
                        <span className="factor-name">Skirmish:</span> Tendency of the player to have a high amount of assists as well as kill participation and damage per minute. Which clearly indicates that he is involved in skirmishes a lot.
                    </li>
                </ul>
            </Typography>

            <Divider
                style={{ background: 'white', borderWidth: 1}}
                variant="middle"
            />
            <Typography id="PCADocumentation-support-title" variant="h3" component="h1" align="left" sx={{ml:5, mt: 10}}>
                Support
            </Typography>
            <Typography id="PCADocumentation-support" variant="p" component="div" align="left" sx={{ml:10, mr: 10, mb: 10, fontSize: 25}}>
                <ul className="PCADocumentation-support">
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Playing w/ jungle:</span> Tendency of the given player to be close to his jungler while leaving his lane while invading and roaming around the map.
                    </li>
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Roaming Jungle:</span> Tendency of the given player to wander within his own jungle.
                    </li>
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Generating Difference:</span> Ability of the player to generate a gold/experience lead over his direct opponent.
                    </li>
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Roaming Top:</span> Tendency of the given player to leave his lane and play around top lane or top river.
                    </li>
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Fighter/DPS:</span> Ability of the given player to have a high kill participation while somewhat having a good damage per minute.
                    </li>
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Roaming Mid:</span> Tendency of the given player to leave his lane and play around the mid lane.
                    </li>
                    <li className="PCADocumentation-support-content">
                        <span className="factor-name">Vision:</span> Ability of the given player to place and destroy wards.
                    </li>
                </ul>
            </Typography>

        </div>
    ) 
}

export default PCADocumentation