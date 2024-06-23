import Form from 'react-bootstrap/Form';

function SelectComp({elementList, defaultValue, setActive}) {
	return (
		<Form.Select aria-label="Default select example" onChange={(e) => setActive(e.target.value)}>
			<option>{defaultValue}</option>
			{elementList.map((element) => (
				<option value={element}>{element}</option>
			))}
		</Form.Select>
	);
}

export default SelectComp;