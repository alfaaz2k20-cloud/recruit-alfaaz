import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function Q1_GalleryBreadth({ onGameEnd, gameId }) {
    const [currentNode, setCurrentNode] = useState('Entrance');
    const [openDoor, setOpenDoor] = useState(null);
    const [unlockProgress, setUnlockProgress] = useState(0);
    const unlockTimerRef = useRef(null);
    const holdIntervalRef = useRef(null);
    
    // N2, N3, N4
    const mapNodes = ['Entrance', 'N2', 'N3', 'N4', 'Exhibit'];
    const doors = {
        'N2': [{ id: 'D1', empty: false, text: "A fascinating history." }, { id: 'D2', empty: true }],
        'N3': [{ id: 'D3', empty: false, text: "A lost artifact." }, { id: 'D4', empty: false, text: "Ancient scrolls." }],
        'N4': [{ id: 'D5', empty: true }]
    };

    const handleMove = (node) => {
        setCurrentNode(node);
        emit_event(gameId, node, 'node_move', {}, { node_id: node });
        if (node === 'Exhibit') {
            emit_event(gameId, 'exhibit', 'exhibit_reached', {}, {});
            onGameEnd();
        }
    };

    const handleUnlockStart = (door) => {
        emit_event(gameId, door.id, 'door_unlock_start', {}, { door_id: door.id });
        setUnlockProgress(0);
        holdIntervalRef.current = setInterval(() => {
            setUnlockProgress(p => p + 10); // visual progress
        }, 300); // roughly 10 ticks for 3s
        
        unlockTimerRef.current = setTimeout(() => {
            clearInterval(holdIntervalRef.current);
            emit_event(gameId, door.id, 'door_unlock_complete', {}, { door_id: door.id });
            emit_event(gameId, door.id, 'panel_open', {}, { door_id: door.id });
            setOpenDoor(door);
            setUnlockProgress(0);
        }, 3000);
    };

    const handleUnlockStop = (door) => {
        clearTimeout(unlockTimerRef.current);
        clearInterval(holdIntervalRef.current);
        setUnlockProgress(0);
    };

    const handleClose = () => {
        if (openDoor) {
            emit_event(gameId, openDoor.id, 'panel_close', {}, { door_id: openDoor.id });
            setOpenDoor(null);
        }
    };

    if (openDoor) {
        return (
            <div style={{ textAlign: 'center', width: '300px' }}>
                <div style={{ padding: '20px', border: '1px solid black', margin: '20px 0', minHeight: '100px' }}>
                    {openDoor.empty ? "This room is empty." : openDoor.text}
                </div>
                <button onClick={handleClose}>Close</button>
            </div>
        );
    }

    const currentIndex = mapNodes.indexOf(currentNode);
    const nextNode = mapNodes[currentIndex + 1];

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Reach the Main Exhibit.</p>
            <h3>Location: {currentNode}</h3>
            
            {doors[currentNode] && doors[currentNode].map((door) => (
                <div key={door.id} style={{ margin: '10px 0' }}>
                    <button 
                        onMouseDown={() => handleUnlockStart(door)}
                        onMouseUp={() => handleUnlockStop(door)}
                        onMouseLeave={() => handleUnlockStop(door)}
                        style={{ width: '100%', padding: '10px' }}
                    >
                        Hold to Unlock {door.id} ({unlockProgress}%)
                    </button>
                </div>
            ))}
            
            {nextNode && (
                <button onClick={() => handleMove(nextNode)} style={{ marginTop: '20px', padding: '10px 20px' }}>
                    Go to {nextNode}
                </button>
            )}
        </div>
    );
}
