import React, { useState } from 'react';
import UploadButton from './uploadButton.js';
import Scatter3D  from './plot.js';

const MyForm = () => {
    const [inputValue, setInputValue] = useState('');

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };
    const handleButtonClick = () => {
        if (inputValue == ''){
            alert('You cannot send an empty value');
        } else {

        }
    };

    return (
        <div className="p-3">
            <div>
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Enter a mobile phone model"
                className="mobile-input mr-3"
            />
            <UploadButton onClick={handleButtonClick}/>
            </div>
            <br/>
            <Scatter3D  />
        </div>

    );
};

export default MyForm;