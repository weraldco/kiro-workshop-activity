import { Router } from 'express';
import { WorkshopController } from '../controllers/workshop.controller';
import { ParticipantController } from '../controllers/participant.controller';
import { ChallengeController } from '../controllers/challenge.controller';

const router = Router();

// Workshop CRUD endpoints
router.post('/workshops', WorkshopController.createWorkshop);
router.get('/workshops', WorkshopController.listWorkshops);
router.patch('/workshops/:id/status', WorkshopController.updateWorkshopStatus);
router.patch('/workshops/:id/signup-flag', WorkshopController.updateSignupFlag);

// Participant endpoints
router.post('/workshops/:id/signup', ParticipantController.signup);
router.get('/workshops/:id/participants', ParticipantController.listParticipants);

// Challenge endpoints
router.post('/workshops/:id/challenges', ChallengeController.createChallenge);
router.get('/workshops/:id/challenges', ChallengeController.listChallenges);
router.get('/challenges/:id', ChallengeController.getChallengeById);

export default router;
