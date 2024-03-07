
import Select from 'react-select';
import "../styles/PlayerSelectComp.css"
import { useState } from 'react';

function PlayerSelectComp({selectedPlayer, setSelectedPlayer}) {

	const playerList = [
		{value: 'aeg_agresivoo', label: "AEG Agresivoo"},
		{value: "aeg_ryuzaki", label: "AEG Ryuzaki"},
		{value: "aeg_nafkelah", label: "AEG Nafkelah"},
		{value: "aeg_hid0", label: "AEG Hid0"},
		{value: "aeg_veignorem", label: "AEG Veignorem"},
		{value: "g2_broken_blade", label: "G2 Broken Blade"},
		{value: "g2_yike", label: "G2 Yike"},
		{value: "g2_caps", label: "G2 Caps"},
		{value: "g2_hans_sama", label: "G2 Hans Sama"},
		{value: "g2_mikyx", label: "G2 Mikyx"}
	]

	return (	
		<>
			<Select
				className="playerSelectComp"
				classNamePrefix="select"
				isClearable={true}
				isSearchable={true}
				options={playerList}
				onChange={(playerName) => setSelectedPlayer(playerName.value)}
				
			/>
		</>
	);
}

export default PlayerSelectComp;
