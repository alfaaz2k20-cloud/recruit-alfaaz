import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function Q2_GalleryDepth({ onGameEnd, gameId }) {
    const [currentNode, setCurrentNode] = useState('N3');
    const [openDoor, setOpenDoor] = useState(null);
    const [showCloser, setShowCloser] = useState(false);
    
    // We start immediately at a node with doors for this shorter game
    const doors = [
        { id: 'D3', text: "A lost artifact.", closerText: "It glows faintly in the dark.", hasCloser: true },
        { id: 'D4', text: "Ancient scrolls.", closerText: "They describe a forgotten ritual.", hasCloser: true }
    ];

    const handleOpen = (door) => {
        emit_event(gameId, door.id, 'panel_open', {}, { door_id: door.id, has_closer: door.hasCloser });
        setOpenDoor(door);
        setShowCloser(false);
    };

    const handleLookCloser = () => {
        emit_event(gameId, openDoor.id, 'look_closer', {}, {});
        setShowCloser(true);
    };

    const handleClose = () => {
        emit_event(gameId, openDoor.id, 'panel_close', {}, { door_id: openDoor.id });
        setOpenDoor(null);
        // Quick exit for game 2 to simulate moving on
        if (openDoor.id === 'D4') {
            onGameEnd();
        }
    };

    if (openDoor) {
        return (
            <div style={{ textAlign: 'center', width: '300px' }}>
                <div style={{ padding: '20px', border: '1px solid black', margin: '20px 0', minHeight: '100px' }}>
                    <p>{openDoor.text}</p>
                    {showCloser && <p style={{ fontStyle: 'italic' }}>{openDoor.closerText}</p>}
                </div>
                {!showCloser && openDoor.hasCloser && (
                    <button onClick={handleLookCloser} style={{ marginRight: '10px' }}>Look closer</button>
                )}
                <button onClick={handleClose}>Close</button>
            </div>
        );
    }

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Explore the gallery.</p>
            <h3>Location: {currentNode}</h3>
            
            {doors.map((door) => (
                <div key={door.id} style={{ margin: '10px 0' }}>
                    <button onClick={() => handleOpen(door)} style={{ width: '100%', padding: '10px' }}>
                        Open {door.id}
                    </button>
                </div>
            ))}
            
            <button onClick={() => onGameEnd()} style={{ marginTop: '20px', padding: '10px 20px' }}>
                Proceed
            </button>
        </div>
    );
}
