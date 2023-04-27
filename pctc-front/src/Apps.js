/* Test Area */

import React from 'react';

function Apps() {
  const handleClick = () => {
    window.open('http://example.com', 'example', 'width=800,height=600');
  };

  return (
    <div>
      <button onClick={handleClick}>Open Popup</button>
    </div>
  );
}

export default Apps;
