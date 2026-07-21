from app.services.document.parser.document_parser import (
    DocumentParser,
)

from app.services.document.snapshot.snapshot_service import (
    SnapshotService,
)

from app.services.document.editor.editor_pipeline import (
    EditorPipeline,
)

from app.services.intelligence.role_detector import (
    RoleDetector,
)

from app.services.intelligence.reasoning.reasoning_engine import (
    ReasoningEngine,
)

from app.services.intelligence.planners.optimization_plan_builder import (
    OptimizationPlanBuilder,
)

from app.services.intelligence.translator.paragraph_update_builder import (
    ParagraphUpdateBuilder,
)


class OptimizationPipeline:
    """
    ResumeOptimizer v3 Pipeline

    Resume
        ↓
    Document Parser
        ↓
    Snapshot
        ↓
    Intelligence
        ↓
    Optimization Plan
        ↓
    Paragraph Updates
        ↓
    Document Editor
        ↓
    Optimized Resume
    """

    @classmethod
    def optimize(
        cls,
        input_file: str,
        job_description,
        output_file: str,
    ):

        # -----------------------------------------
        # Parse Resume
        # -----------------------------------------

        document_model = DocumentParser.parse(
            input_file
        )

        # -----------------------------------------
        # Build Snapshot
        # -----------------------------------------

        snapshot_service = SnapshotService.from_document(
            document_model
        )

        snapshot = snapshot_service.snapshot

        # -----------------------------------------
        # Detect Resume Role
        # -----------------------------------------

        detected_role = RoleDetector.detect(
            snapshot
        )

        print("\n" + "=" * 60)
        print("DETECTED ROLE")
        print("=" * 60)
        print(detected_role)

        # -----------------------------------------
        # Analyze Resume vs Job Description
        # -----------------------------------------

        reasoning = ReasoningEngine.analyze(
            snapshot,
            job_description,
        )

        # -----------------------------------------
        # Build Optimization Plan
        # -----------------------------------------

        plan = OptimizationPlanBuilder.build(
            snapshot,
            job_description,
        )

        # -----------------------------------------
        # Build Paragraph Updates
        # -----------------------------------------

        paragraph_updates = ParagraphUpdateBuilder.build(
            snapshot,
            plan,
            job_description,
        )

        # -----------------------------------------
        # Apply Updates to Original DOCX
        # -----------------------------------------

        EditorPipeline.apply(
            input_file=input_file,
            output_file=output_file,
            paragraph_updates=paragraph_updates,
        )

        # -----------------------------------------
        # Pipeline Result
        # -----------------------------------------

        return {
            "snapshot": snapshot,
            "role": detected_role,
            "reasoning": reasoning,
            "plan": plan,
            "paragraph_updates": paragraph_updates,
            "output": output_file,
        }