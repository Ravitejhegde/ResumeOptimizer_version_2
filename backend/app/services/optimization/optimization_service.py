from __future__ import annotations

import logging
import uuid

from pathlib import Path

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceNotFoundError,
)

from app.database.models.optimization_job import (
    OptimizationJob,
)

from app.database.models.generated_resume import (
    GeneratedResume,
)

from app.database.repositories.resume_repository import (
    ResumeRepository,
)

from app.database.repositories.optimization_job_repository import (
    OptimizationJobRepository,
)

from app.engine.orchestrator import (
    ResumeOptimizationEngine,
)

from app.engine.models.optimizer.optimization_request import (
    OptimizationRequest,
)

from app.engine.reader.document_reader import (
    DocumentReader,
)



logger = logging.getLogger(__name__)



class OptimizationService:
    """
    Coordinates resume optimization workflow.

    Pipeline:

        Database Resume
              |
              v
        DocumentReader
              |
              v
        Document Model
              |
              v
        OptimizationRequest
              |
              v
        ResumeOptimizationEngine
              |
              v
        AI Optimization
              |
              v
        Writer
              |
              v
        Generated Resume
    """



    def __init__(
        self,
        db: Session,
        engine: ResumeOptimizationEngine,
    ) -> None:


        self._resume_repository = (
            ResumeRepository(db)
        )


        self._job_repository = (
            OptimizationJobRepository(db)
        )


        self._db = db


        self._engine = engine


        self._reader = (
            DocumentReader()
        )



    async def optimize(
        self,
        resume_id: str,
        job_description: str,
        selected_skills: list[str],
    ) -> GeneratedResume:


        logger.info(
            "[OptimizationService] Starting resume=%s",
            resume_id,
        )



        resume = (
            self._resume_repository.get(
                resume_id
            )
        )



        if resume is None:

            raise ResourceNotFoundError(
                "Resume not found."
            )



        job = OptimizationJob(

            resume_id=resume.id,

            job_description=job_description,

            selected_skills=",".join(
                selected_skills
            ),

            status="running",

        )



        self._job_repository.create(
            job
        )


        self._db.flush()



        try:


            source = Path(
                resume.file_path
            )


            if not source.exists():

                raise FileNotFoundError(
                    str(source)
                )



            output_file = (

                source.parent

                /

                (
                    f"{source.stem}"
                    f"_optimized_"
                    f"{uuid.uuid4().hex[:8]}"
                    f"{source.suffix}"
                )

            )



            # ----------------------------------
            # Read DOCX into engine model
            # ----------------------------------

            document = (
                self._reader.read(
                    str(source)
                )
            )



            logger.info(
                "[OptimizationService] Document loaded."
            )



            # ----------------------------------
            # Build optimizer request
            # ----------------------------------

            request = OptimizationRequest(

                document=document,

                plan=None,

                request_id=str(job.id),

                preserve_formatting=True,


    # IMPORTANT
                job_context={
                "job_description": job_description,
                "selected_skills": selected_skills,
            },


                knowledge_context={
        "selected_skills": selected_skills,
    },


                metadata={

                "job_description":
                    job_description,

                "selected_skills":
                    selected_skills,

                "source_file":
                    str(source),

                "output_file":
                    str(output_file),

            },

        )



            # ----------------------------------
            # Execute optimization
            # ----------------------------------

            result = await (

                self._engine.optimize(
                    request
                )

            )



            if not result:

                raise RuntimeError(
                    "Optimizer returned empty result."
                )



            logger.info(
                "[OptimizationService] "
                "Optimization completed."
            )



            # ----------------------------------
            # Writer step
            # ----------------------------------

            # Writer integration will create this file.
            # Currently engine result only.


            if not output_file.exists():

                logger.warning(

                    "[OptimizationService] "
                    "Output file not generated yet."

                )



            job.status = "completed"



            generated = GeneratedResume(

                optimization_job_id=job.id,

                filename=output_file.name,

                file_path=str(output_file),

                file_size=(

                    output_file.stat().st_size

                    if output_file.exists()

                    else 0

                ),

            )



            self._db.add(
                generated
            )


            self._db.commit()



            logger.info(

                "[OptimizationService] "
                "Generated resume=%s",

                generated.id,

            )



            return generated



        except Exception as exc:


            job.status = "failed"


            self._db.commit()



            logger.exception(

                "[OptimizationService] "
                "Optimization failed."

            )


            raise exc