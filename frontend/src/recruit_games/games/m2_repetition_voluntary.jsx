import React, { useState, useEffect } from 'react';
import { emit_event } from '../telemetry';

export default function M2_RepetitionVoluntary({ onGameEnd, gameId }) {
    const [stamps, setStamps] = useState(0);
    const [hasFlyer, setHasFlyer] = useState(false);
    const [switched, setSwitched] = useState(false);
    
    const handlePick = () => {
        if (!hasFlyer && stamps < 40) {
            setHasFlyer(true);
            emit_event(gameId, 'block1', 'flyer_pick', {}, {});
        }
    };

    const handleStamp = () => {
        if (hasFlyer) {
            const newCount = stamps + 1;
            setStamps(newCount);
            setHasFlyer(false);
            emit_event(gameId, 'block1', 'stamp', {}, { unit_index: newCount });
            
            if (newCount === 10) {
                emit_event(gameId, 'block1', 'min_reached', {}, {});
            }
        }
    };

    const handleFinish = () => {
        emit_event(gameId, 'block1', 'finish_press', {}, {});
        onGameEnd();
    };

    const handleSwitch = () => {
        setSwitched(true);
        emit_event(gameId, 'block1', 'harder_option_chosen', {}, {});
    };

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Stamp 10 flyers to finish this part.</p>
            
            <div style={{ margin: '20px 0', height: '100px', border: '1px solid #ccc', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {hasFlyer ? '📄' + (switched ? ' (Sorting...)' : ' (Ready to stamp)') : 'No flyer'}
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                <button onClick={handlePick} disabled={hasFlyer || stamps >= 40}>Pick Flyer</button>
                <button onClick={handleStamp} disabled={!hasFlyer}>Stamp</button>
            </div>
            
            {stamps < 10 ? (
                <p>{stamps} of 10</p>
            ) : (
                <div style={{ marginTop: '20px' }}>
                    <p>Your required assessment is complete. You may finish now.</p>
                    <button onClick={handleFinish} style={{ padding: '10px 20px', marginBottom: '10px' }}>Finish</button>
                    {!switched && (
                        <div>
                            <button onClick={handleSwitch} style={{ padding: '5px' }}>
                                Switch to sorting by district (slower)
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
