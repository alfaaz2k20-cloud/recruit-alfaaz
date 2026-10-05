import React, { useState } from 'react';
import { GameShell } from './shell';
import F1 from './games/f1_frequency';
import F2 from './games/f2_frequency_ambiguous';
import A1 from './games/a1_archive_rule';
import A2 from './games/a2_archive_exception';
import C1 from './games/c1_canvas_sharing';
import C2 from './games/c2_canvas_coordination';
import E1 from './games/e1_grid_reversal';
import E2 from './games/e2_grid_disruption';
import Q1 from './games/q1_gallery_breadth';
import Q2 from './games/q2_gallery_depth';
import CR1 from './games/cr1_broken_tool_build';
import CR3 from './games/cr3_broken_tool_experiment';
import M1 from './games/m1_repetition_mandatory';
import M2 from './games/m2_repetition_voluntary';

const GAMES = [
    { id: 'F1', component: F1, title: 'Frequency', duration: 18, instructions: 'Tune the channel. A producer is listening.' },
    { id: 'F2', component: F2, title: 'Frequency II', duration: 16, instructions: 'Tune the channel again.' },
    { id: 'A1', component: A1, title: 'Archive', duration: 15, instructions: 'File each item into the correct folder.' },
    { id: 'A2', component: A2, title: 'Archive II', duration: 15, instructions: 'File each item. You can flag exceptions.' },
    { id: 'C1', component: C1, title: 'Canvas', duration: 20, instructions: 'Paint your half. You can send paint to your partner.' },
    { id: 'C2', component: C2, title: 'Canvas II', duration: 20, instructions: 'Paint your half. Coordinate with partner.' },
    { id: 'E1', component: E1, title: 'Grid', duration: 24, instructions: 'Sort shapes left or right.' },
    { id: 'E2', component: E2, title: 'Grid II', duration: 20, instructions: 'Sort shapes left or right.' },
    { id: 'Q1', component: Q1, title: 'Gallery', duration: 25, instructions: 'Reach the Main Exhibit.' },
    { id: 'Q2', component: Q2, title: 'Gallery II', duration: 16, instructions: 'Explore the gallery.' },
    { id: 'CR1', component: CR1, title: 'Build', duration: 30, instructions: 'Get the orb to the pad. Use what you have.' },
    { id: 'CR3', component: CR3, title: 'Experiment', duration: 30, instructions: 'Get the orb to the pad. Watch out for traps.' },
    { id: 'M1', component: M1, title: 'Repetition', duration: 18, instructions: 'Stamp 10 flyers to finish this part.' },
    { id: 'M2', component: M2, title: 'Repetition II', duration: 18, instructions: 'Stamp 10 flyers.' }
];

export default function GameSequence() {
    const [currentIndex, setCurrentIndex] = useState(0);

    const handleComplete = () => {
        if (currentIndex < GAMES.length - 1) {
            setCurrentIndex(i => i + 1);
        } else {
            alert('All games complete! Check console or network for evaluation.');
        }
    };

    const currentGame = GAMES[currentIndex];
    if (!currentGame) return <div>Done</div>;

    const GameComponent = currentGame.component;

    return (
        <GameShell 
            key={currentGame.id} // force remount
            gameId={currentGame.id}
            title={currentGame.title}
            duration={currentGame.duration}
            instructions={currentGame.instructions}
            onComplete={handleComplete}
        >
            <GameComponent />
        </GameShell>
    );
}
