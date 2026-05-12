from pyautocad import Autocad
import time

def generate_drawing_summary():

    try:

        acad = Autocad(create_if_not_exists=True)

        # Allow AutoCAD time to stabilize
        time.sleep(3)

        lines = 0
        circles = 0
        arcs = 0
        polylines = 0
        text_objects = 0

        for obj in acad.iter_objects():

            try:

                name = obj.ObjectName

                if name == "AcDbLine":
                    lines += 1

                elif name == "AcDbCircle":
                    circles += 1

                elif name == "AcDbArc":
                    arcs += 1

                elif name in [
                    "AcDbPolyline",
                    "AcDb2dPolyline",
                    "AcDb3dPolyline"
                ]:
                    polylines += 1

                elif name in [
                    "AcDbText",
                    "AcDbMText"
                ]:
                    text_objects += 1

            except:
                continue

        total = (
            lines +
            circles +
            arcs +
            polylines +
            text_objects
        )

        summary = f"""
Drawing Summary

Lines: {lines}
Circles: {circles}
Arcs: {arcs}
Polylines: {polylines}
Text Objects: {text_objects}

Total Objects: {total}
"""

        return summary

    except Exception as e:

        return f"AutoCAD connection error: {str(e)}"
