#pragma once

class UWorld;

/** Explicit Development-only experiment. Never activated by a map or gameplay class. */
namespace PMSoftShadowTest
{
 bool Enable(UWorld* World);
 void Stop();
}
