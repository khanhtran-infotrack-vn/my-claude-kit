#!/usr/bin/env python3
"""
User Story Generator with INVEST Criteria
Creates well-formed user stories with acceptance criteria
"""

import json
from typing import Dict, List, Tuple


class UserStoryGenerator:
    """Generate INVEST-compliant user stories"""

    def __init__(self):
        self.personas = {
            "end_user": {
                "name": "End User",
                "needs": ["efficiency", "simplicity", "reliability", "speed"],
                "context": "daily usage of core features",
            },
            "admin": {
                "name": "Administrator",
                "needs": ["control", "visibility", "security", "configuration"],
                "context": "system management and oversight",
            },
            "power_user": {
                "name": "Power User",
                "needs": [
                    "advanced features",
                    "automation",
                    "customization",
                    "shortcuts",
                ],
                "context": "expert usage and workflow optimization",
            },
            "new_user": {
                "name": "New User",
                "needs": ["guidance", "learning", "safety", "clarity"],
                "context": "first-time experience and onboarding",
            },
        }

        self.story_templates = {
            "feature": "As a {persona}, I want to {action} so that {benefit}",
            "improvement": "As a {persona}, I need {capability} to {achieve_goal}",
            "fix": "As a {persona}, I expect {behavior} when {condition}",
            "integration": "As a {persona}, I want to {integrate} so that {workflow}",
        }

        self.acceptance_criteria_patterns = [
            "Given {precondition}, When {action}, Then {outcome}",
            "Should {behavior} when {condition}",
            "Must {requirement} to {achieve}",
            "Can {capability} without {negative_outcome}",
        ]

    def generate_epic_stories(self, epic: Dict) -> List[Dict]:
        """Break down epic into user stories"""
        stories = []

        # Analyze epic for key components
        epic_name = epic.get("name", "Feature")
        epic_description = epic.get("description", "")
        personas = epic.get("personas", ["end_user"])
        scope = epic.get("scope", [])

        # Generate stories for each persona and scope item
        for persona in personas:
            for i, scope_item in enumerate(scope):
                story = self.generate_story(
                    persona=persona, feature=scope_item, epic=epic_name, index=i + 1
                )
                stories.append(story)

        # Add enabler stories (technical, infrastructure)
        if epic.get("technical_requirements"):
            for req in epic["technical_requirements"]:
                enabler = self.generate_enabler_story(req, epic_name)
                stories.append(enabler)

        return stories

    def generate_story(self, persona: str, feature: str, epic: str, index: int) -> Dict:
        """Generate a single user story"""

        persona_data = self.personas.get(persona, self.personas["end_user"])

        # Create story
        story = {
            "id": f"{epic[:3].upper()}-{index:03d}",
            "type": "story",
            "title": self._generate_title(feature),
            "narrative": self._generate_narrative(persona_data, feature),
            "acceptance_criteria": self._generate_acceptance_criteria(feature),
            "estimation": self._estimate_complexity(feature),
            "priority": self._determine_priority(persona, feature),
            "dependencies": [],
            "invest_check": self._check_invest_criteria(feature),
        }

        return story

    def generate_enabler_story(self, requirement: str, epic: str) -> Dict:
        """Generate technical enabler story"""

        return {
            "id": f"{epic[:3].upper()}-E{len(requirement):02d}",
            "type": "enabler",
            "title": f"Technical: {requirement}",
            "narrative": f"As a developer, I need to {requirement} to enable user features",
            "acceptance_criteria": [
                f"Technical requirement {requirement} is implemented",
                "All tests pass",
                "Documentation is updated",
                "No regression in existing functionality",
            ],
            "estimation": 5,  # Default medium complexity
            "priority": "high",
            "dependencies": [],
            "invest_check": {
                "independent": True,
                "negotiable": False,  # Technical requirements often non-negotiable
                "valuable": True,
                "estimable": True,
                "small": True,
                "testable": True,
            },
        }

    def _generate_title(self, feature: str) -> str:
        """Generate concise story title"""
        # Simplify feature description to title
        words = feature.split()[:5]
        return " ".join(words).title()

    def _generate_narrative(self, persona: Dict, feature: str) -> str:
        """Generate story narrative in standard format"""

        template = self.story_templates["feature"]

        action = self._extract_action(feature)
        benefit = self._extract_benefit(feature, persona["needs"])

        return template.format(persona=persona["name"], action=action, benefit=benefit)

    def _generate_acceptance_criteria(self, feature: str) -> List[str]:
        """Generate acceptance criteria"""

        criteria = []

        # Happy path
        criteria.append(
            f"Given user has access, When they {self._extract_action(feature)}, Then {self._extract_outcome(feature)}"
        )

        # Validation
        criteria.append(f"Should validate input before processing")

        # Error handling
        criteria.append(f"Must show clear error message when action fails")

        # Performance
        criteria.append(f"Should complete within 2 seconds")

        # Accessibility
        criteria.append(f"Must be accessible via keyboard navigation")

        return criteria

    def _extract_action(self, feature: str) -> str:
        """Extract action from feature description"""
        action_verbs = [
            "create",
            "view",
            "edit",
            "delete",
            "share",
            "export",
            "import",
            "configure",
            "search",
            "filter",
        ]

        feature_lower = feature.lower()
        for verb in action_verbs:
            if verb in feature_lower:
                return feature_lower

        return f"use {feature.lower()}"

    def _extract_benefit(self, feature: str, needs: List[str]) -> str:
        """Extract benefit based on feature and persona needs"""

        feature_lower = feature.lower()

        if "save" in feature_lower or "quick" in feature_lower:
            return "I can save time and work more efficiently"
        elif "share" in feature_lower or "collab" in feature_lower:
            return "I can collaborate with my team effectively"
        elif "report" in feature_lower or "analyt" in feature_lower:
            return "I can make data-driven decisions"
        elif "automat" in feature_lower:
            return "I can reduce manual work and errors"
        else:
            return f"I can achieve my goals related to {needs[0]}"

    def _extract_outcome(self, feature: str) -> str:
        """Extract expected outcome"""
        return f"the {feature.lower()} is successfully completed"

    def _estimate_complexity(self, feature: str) -> int:
        """Estimate story points based on complexity indicators"""

        feature_lower = feature.lower()

        # Complexity indicators
        complexity = 3  # Base complexity

        if any(
            word in feature_lower for word in ["simple", "basic", "view", "display"]
        ):
            complexity = 1
        elif any(word in feature_lower for word in ["create", "edit", "update"]):
            complexity = 3
        elif any(
            word in feature_lower
            for word in ["complex", "advanced", "integrate", "migrate"]
        ):
            complexity = 8
        elif any(
            word in feature_lower for word in ["redesign", "refactor", "architect"]
        ):
            complexity = 13

        return complexity

    def _determine_priority(self, persona: str, feature: str) -> str:
        """Determine story priority"""

        feature_lower = feature.lower()

        # Critical features
        if any(
            word in feature_lower for word in ["security", "fix", "critical", "broken"]
        ):
            return "critical"

        # High priority for primary personas
        if persona in ["end_user", "admin"]:
            if any(word in feature_lower for word in ["core", "essential", "primary"]):
                return "high"

        # Medium for improvements
        if any(word in feature_lower for word in ["improve", "enhance", "optimize"]):
            return "medium"

        # Low for nice-to-haves
        return "low"

    def _check_invest_criteria(self, feature: str) -> Dict[str, bool]:
        """Check INVEST criteria compliance"""

        return {
            "independent": not any(
                word in feature.lower() for word in ["after", "depends", "requires"]
            ),
            "negotiable": True,  # Most features can be negotiated
            "valuable": True,  # Assume value if it made it to backlog
            "estimable": len(feature.split()) < 20,  # Can estimate if not too vague
            "small": self._estimate_complexity(feature) <= 8,  # 8 points or less
            "testable": not any(
                word in feature.lower() for word in ["maybe", "possibly", "somehow"]
            ),
        }

    def generate_sprint_stories(self, capacity: int, backlog: List[Dict]) -> Dict:
        """Generate stories for a sprint based on capacity"""

        sprint = {
            "capacity": capacity,
            "committed": [],
            "stretch": [],
            "total_points": 0,
            "utilization": 0,
        }

        # Sort backlog by priority and size
        sorted_backlog = sorted(
            backlog,
            key=lambda x: (
                {"critical": 0, "high": 1, "medium": 2, "low": 3}[x["priority"]],
                x["estimation"],
            ),
        )

        # Fill sprint
        for story in sorted_backlog:
            if sprint["total_points"] + story["estimation"] <= capacity:
                sprint["committed"].append(story)
                sprint["total_points"] += story["estimation"]
            elif sprint["total_points"] + story["estimation"] <= capacity * 1.2:
                sprint["stretch"].append(story)

        sprint["utilization"] = round((sprint["total_points"] / capacity) * 100, 1)

        return sprint

    def format_story_output(self, story: Dict) -> str:
        """Format story for display"""

        output = []
        output.append(f"USER STORY: {story['id']}")
        output.append("=" * 40)
        output.append(f"Title: {story['title']}")
        output.append(f"Type: {story['type']}")
        output.append(f"Priority: {story['priority'].upper()}")
        output.append(f"Points: {story['estimation']}")
        output.append("")
        output.append("Story:")
        output.append(story["narrative"])
        output.append("")
        output.append("Acceptance Criteria:")
        for i, criterion in enumerate(story["acceptance_criteria"], 1):
            output.append(f"  {i}. {criterion}")
        output.append("")
        output.append("INVEST Checklist:")
        for criterion, passed in story["invest_check"].items():
            status = "✓" if passed else "✗"
            output.append(f"  {status} {criterion.capitalize()}")

        return "\n".join(output)


def create_sample_epic():
    """Create a sample epic for testing"""
    return {
        "name": "User Dashboard",
        "description": "Create a comprehensive dashboard for users to view their data",
        "personas": ["end_user", "power_user"],
        "scope": [
            "View key metrics and KPIs",
            "Customize dashboard layout",
            "Export dashboard data",
            "Share dashboard with team members",
            "Set up automated reports",
        ],
        "technical_requirements": [
            "Implement caching for performance",
            "Set up real-time data pipeline",
        ],
    }


def save_stories_to_file(stories, epic_name, output_path=None):
    """Save user stories to a markdown file"""
    import os
    from datetime import datetime

    generator = UserStoryGenerator()

    # Create output directory if it doesn't exist
    if output_path is None:
        # Default to docs/user-stories/
        output_dir = os.path.join(os.getcwd(), "docs", "user-stories")
    else:
        output_dir = os.path.dirname(output_path)

    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    if output_path is None:
        timestamp = datetime.now().strftime("%y%m%d-%H%M")
        epic_slug = epic_name.lower().replace(" ", "-")
        filename = f"{timestamp}-{epic_slug}.md"
        output_path = os.path.join(output_dir, filename)

    # Calculate summary statistics
    total_points = sum(s["estimation"] for s in stories)
    priority_counts = {}
    for priority in ["critical", "high", "medium", "low"]:
        priority_counts[priority] = len(
            [s for s in stories if s["priority"] == priority]
        )

    # Generate markdown content
    content = []
    content.append(f"# User Stories: {epic_name}\n")
    content.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    content.append(f"**Total Stories**: {len(stories)}")
    content.append(f"**Total Story Points**: {total_points}")
    content.append(f"**Estimated Time**: {_estimate_time_range(total_points)}\n")

    content.append("## Priority Breakdown\n")
    for priority, count in priority_counts.items():
        if count > 0:
            content.append(f"- **{priority.capitalize()}**: {count} stories")
    content.append("")

    content.append("## Stories\n")

    for story in stories:
        content.append(f"### {story['id']}: {story['title']}\n")
        content.append(f"**Type**: {story['type']}")
        content.append(f"**Priority**: {story['priority']}")
        content.append(f"**Story Points**: {story['estimation']}")
        content.append(
            f"**Estimated Time**: {_estimate_time_from_points(story['estimation'])}\n"
        )
        content.append("**Story**:")
        content.append(story["narrative"] + "\n")
        content.append("**Acceptance Criteria**:")
        for i, criterion in enumerate(story["acceptance_criteria"], 1):
            content.append(f"{i}. {criterion}")
        content.append("")
        content.append("**INVEST Check**:")
        for criterion, passed in story["invest_check"].items():
            status = "✓" if passed else "✗"
            content.append(f"- {status} {criterion.capitalize()}")
        content.append("\n---\n")

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    return output_path


def _estimate_time_from_points(points):
    """Convert story points to time estimate"""
    time_map = {
        1: "2-4 hours",
        2: "4-8 hours",
        3: "0.5-1 day",
        5: "1-2 days",
        8: "2-3 days",
        13: "3-5 days",
    }
    return time_map.get(points, f"{points} points")


def _estimate_time_range(total_points):
    """Convert total points to time range"""
    # Using 1 point = 3 hours average
    min_days = (total_points * 2) / 8  # 2 hours per point, 8 hours per day
    max_days = (total_points * 4) / 8  # 4 hours per point, 8 hours per day

    if max_days < 1:
        return f"{int(min_days * 8)}-{int(max_days * 8)} hours"
    elif max_days < 5:
        return f"{min_days:.1f}-{max_days:.1f} days"
    elif max_days < 20:
        min_weeks = min_days / 5
        max_weeks = max_days / 5
        return f"{min_weeks:.1f}-{max_weeks:.1f} weeks"
    else:
        min_months = min_days / 20
        max_months = max_days / 20
        return f"{min_months:.1f}-{max_months:.1f} months"


def main():
    import sys

    generator = UserStoryGenerator()

    # Check for --save or -s flag
    save_to_file = "--save" in sys.argv or "-s" in sys.argv
    output_path = None

    if save_to_file:
        # Check if custom path provided after --save/-s flag
        save_idx = (
            sys.argv.index("--save") if "--save" in sys.argv else sys.argv.index("-s")
        )
        if (
            save_idx + 1 < len(sys.argv)
            and not sys.argv[save_idx + 1].startswith("-")
            and sys.argv[save_idx + 1] != "sprint"
        ):
            output_path = sys.argv[save_idx + 1]

    # Remove flags from argv for processing
    args = [
        arg
        for arg in sys.argv[1:]
        if arg not in ["--save", "-s"] and not (output_path and arg == output_path)
    ]

    if len(args) > 0 and args[0] == "sprint":
        # Generate sprint planning
        capacity = int(args[1]) if len(args) > 1 else 30

        # Create sample backlog
        epic = create_sample_epic()
        backlog = generator.generate_epic_stories(epic)

        # Plan sprint
        sprint = generator.generate_sprint_stories(capacity, backlog)

        print("=" * 60)
        print("SPRINT PLANNING")
        print("=" * 60)
        print(f"Sprint Capacity: {sprint['capacity']} points")
        print(f"Committed: {sprint['total_points']} points ({sprint['utilization']}%)")
        print(
            f"Stories: {len(sprint['committed'])} committed + {len(sprint['stretch'])} stretch"
        )
        print("\n📋 COMMITTED STORIES:\n")

        for story in sprint["committed"]:
            print(
                f"  [{story['priority'][:1].upper()}] {story['id']}: {story['title']} ({story['estimation']}pts)"
            )

        if sprint["stretch"]:
            print("\n🎯 STRETCH GOALS:\n")
            for story in sprint["stretch"]:
                print(
                    f"  [{story['priority'][:1].upper()}] {story['id']}: {story['title']} ({story['estimation']}pts)"
                )

    else:
        # Generate stories for epic
        epic = create_sample_epic()
        stories = generator.generate_epic_stories(epic)

        # Save to file if requested
        if save_to_file:
            saved_path = save_stories_to_file(stories, epic["name"], output_path)
            print(f"✓ User stories saved to: {saved_path}\n")

        print(f"Generated {len(stories)} stories from epic: {epic['name']}\n")

        # Display first 3 stories in detail
        for story in stories[:3]:
            print(generator.format_story_output(story))
            print("\n")

        # Summary of all stories
        print("=" * 60)
        print("BACKLOG SUMMARY")
        print("=" * 60)
        total_points = sum(s["estimation"] for s in stories)
        print(f"Total Stories: {len(stories)}")
        print(f"Total Points: {total_points}")
        print(f"Average Size: {total_points / len(stories):.1f} points")
        print("\nPriority Breakdown:")
        for priority in ["critical", "high", "medium", "low"]:
            count = len([s for s in stories if s["priority"] == priority])
            if count > 0:
                print(f"  {priority.capitalize()}: {count} stories")


if __name__ == "__main__":
    main()
